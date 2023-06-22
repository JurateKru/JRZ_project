from typing import Any, Optional, Type
from django.utils.translation import gettext_lazy as _
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, FileResponse
from django import forms
from . models import Application, ApplicationInstance, Employee
from . forms import ApplicationInstanceForm
from user_profile.models import Profile, ManagerProfile
from . process import html_to_pdf
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa 
from django.template.loader import render_to_string

User = get_user_model()

def index(request):
    return render(request, 'hr_system/index.html')


def about_us(request):
    return render(request, 'hr_system/about_us.html')


class ExportPdfView(generic.DetailView):
    model= ApplicationInstance 
    template_name= f"hr_system/export_pdf.html"
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['application'] = get_object_or_404(ApplicationInstance, id=self.kwargs['pk'])
        return context


def render_pdf_view(request, **kwargs):
    obj = get_object_or_404(ApplicationInstance, id=kwargs['pk'])
    #obj = get_object_or_404(Application, pk=kwargs['pk'])
    # obj_profile = Profile.objects.filter(user=request.user).get()

    template_path = f"hr_system/export_pdf.html"
    
    

    context = {'application': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    #template = get_template(template_path)
    
    html = render_to_string(template_path, context)
    #html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


class ApplicationListView(generic.ListView):
    model = Application
    template_name = 'hr_system/application_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(
                Q(id__icontains=query),
                Q(tempalte__icontains=query),
                Q(date_created__icontains=query),
                Q(status__icontains=query)                      
            )
        return qs
    
class ApplicationFormView(generic.CreateView):
    model = ApplicationInstance
    form_class = ApplicationInstanceForm
    template_name = 'hr_system/application_instance.html'
    success_url = reverse_lazy('application_list')

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['application'] = self.get_application()
        return context
    
    # Get Aplications object by Application.id(passed throught urls.py)
    def get_application(self):
        return get_object_or_404(Application, pk=self.kwargs['pk'])
    
    def get_user_profile(self):
        return Profile.objects.filter(user=self.request.user).get()

    # Create initial form instance populate with needed fields 
    def get_form(self, form_class= form_class) -> BaseModelForm:
        form = super().get_form(form_class)
        
        # initial fields
        form.fields['start_date'] = forms.DateField(label=_("Start Date"), widget=forms.widgets.DateInput(
    attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}))
        form.fields['manager'] = forms.CharField(label=_("manager"))
        
        
        if self.request.user.is_authenticated:
            
            form.fields['manager'] = forms.CharField(label=_("manager"), widget=forms.HiddenInput(), required=False)
            form.fields['full_name'] = forms.CharField(label=_("full name"), widget=forms.HiddenInput(), required=False)
        else:
            form.fields['full_name'] = forms.CharField(label=_("full name"))
            form.fields['manager'] = forms.CharField(label=_("manager"))


        if self.get_application().title == "Vacation": # Atostogos
            form.fields['end_date'] = forms.DateField(label=_("End Date"), widget=forms.widgets.DateInput(
        attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}))
            form.fields['payout_before'] = forms.ChoiceField(label=_("Payment"), choices=(
                ("along with the regular salary payment", _("along with the regular salary payment")), 
                ("before requested vacation leave", _("before the requested vacation leave")), ))
            # form.fields['start_date'] = forms.DateField(label=_("Start Date"))
            # form.fields['full_name'] = forms.CharField(label=_("full name"))
            # form.fields['manager'] = forms.CharField(label=_("manager"))
        
        if self.get_application().title == "Taxes": # Mokesciai
            form.fields['npd'] = forms.BooleanField(label=_("npd"), required=False)
            # form.fields['start_date'] = forms.DateField(label=_("start_date"))
            # form.fields['full_name'] = forms.CharField(label=_("full name"))
            # form.fields['manager'] = forms.CharField(label=_("manager"))

        if self.get_application().title == "Parent Day-off":
            form.fields['parental_status'] = forms.ChoiceField(label=_("Parental Day-off"), choices=(
        ("I am raising 1 child under 12 years old", _("Raising 1 child under 12 years old")),
        ("I am raising 2 or more children under 12 years old", _("Raising 2 or more children under 12 years old")),
        ("I am raising 3 or more children under 12 years old", _("Raising 3 or more children under 12 years old")),
        ("I am raising 1 child with disabilities", _("Raising 1 child with disabilities")),
        ("I am raising 2 or more children with disabilities", _("Raising 2 or more children with disabilities"))
        ) )
            # form.fields['full_name'] = forms.CharField(label=_("full name"))
            # form.fields['manager'] = forms.CharField(label=_("manager"))
            # form.fields['start_date'] = forms.DateField(label=_("Start Date"))
        
        if self.get_application().title == "Terminate":
            return form
            # form.fields['full_name'] = forms.CharField(label=_("full name"))
            # form.fields['manager'] = forms.CharField(label=_("manager"))
            # form.fields['start_date'] = forms.DateField(label=_("Start Date"))
        return form

    # gets populated form, passes throught generate_description() returns form with values
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.application = self.get_application()
        instance.save()
        
        form.instance.content = self.generate_description(form.cleaned_data)
        form.instance.applicant = self.request.user
        return super().form_valid(form)

    # Populates form with values(user inputs)
    def generate_description(self, form_data):
        form = self.get_form(self.form_class)
        
        template = self.get_application().description
        
        # Dynamically create multiple variables
        for key in form.fields.keys():

            locals()[key] = form_data[key]
            if key == 'npd':
                if locals()[key] == True:
                    locals()[key] = 'taikyti'
                else:
                    locals()[key] = 'netaikyti'
            if self.request.user.is_authenticated:    
                if key == 'full_name':
                    locals()[key] =  self.get_user_profile().employee.f_name + ' ' + self.get_user_profile().employee.l_name  # self.request.user.first_name + ' ' + self.request.user.last_name
                if key == 'manager':
                    locals()[key] = self.get_user_profile().manager.f_name + ' ' + self.get_user_profile().manager.l_name
        # print(locals())
    
        # **locals() syntax, which unpacks the dynamically created variables as keyword arguments.
        description = template.format(**locals())

        return description
    
class UserApplicationListView(LoginRequiredMixin, generic.ListView):
    model = ApplicationInstance
    template_name = 'hr_system/user_application_instances.html'   

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(applicant=self.request.user)
        return qs
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['user_applications'] = ApplicationInstance.objects.filter(applicant=self.request.user)
        return context
    

class UserApplicationDetailView(LoginRequiredMixin, generic.DetailView):
    model = ApplicationInstance
    template_name = 'hr_system/user_application_detail.html' 

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['application'] = get_object_or_404(ApplicationInstance, id=self.kwargs['pk'])
        return context
    
class DepartmentApplicationListView(LoginRequiredMixin, generic.ListView):
    model = ApplicationInstance
    template_name = 'hr_system/department_application_instances.html'   

    def get_queryset(self) -> QuerySet[Any]:
        user_profile = ManagerProfile.objects.get(user=self.request.user)
        department_employees = user_profile.employees.all().values_list('user', flat=True)
        qs = super().get_queryset()
        qs = qs.filter(applicant__in=department_employees)
        return qs
    
    # def get_context_data(self, **kwargs: Any):
    #     context = super().get_context_data(**kwargs)
    #     user_profile = ManagerProfile.objects.get(user=self.request.user)
    #     department_employees = user_profile.employees.all()
    #     context['user_applications'] = ApplicationInstance.objects.filter(applicant__employee__in=department_employees)
    #     return context    
