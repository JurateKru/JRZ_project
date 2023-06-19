from typing import Optional, Type
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404
from django.views import generic
from . models import Application, ApplicationInstance
from django.db.models import Q
from . forms import ApplicationInstanceForm
from django.urls import reverse, reverse_lazy

def index(request):
    return render(request, 'hr_system/index.html')

def about_us(request):
    return render(request, 'hr_system/about_us.html')

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

# class ApplicationFormView(generic.CreateView):
#     model = ApplicationInstance
#     form_class = ApplicationInstanceForm
#     template_name = 'hr_system/application_instance.html'
#     success_url = reverse_lazy('application_list')

#     def get_initial(self):
#         initial = super().get_initial()
#         obj = get_object_or_404(Application, pk=self.kwargs['pk'])
#         initial['content'] = obj.description
#         return initial
    
class ApplicationFormView(generic.CreateView):
    model = ApplicationInstance
    form_class = ApplicationInstanceForm
    template_name = 'hr_system/application_instance.html'
    success_url = reverse_lazy('application_list')

    # def get_form(self, form_class= form_class) -> BaseModelForm:
    #     form = super().get_form(form_class)
    #     application = get_object_or_404(Application, pk=self.kwargs['pk'])
    #     if form.application == 1:
    #         # form = form(initial={'client': forms.HiddenInput() })
    #         form.fields['client'].widget = forms.HiddenInput() 
    #     return form

    def form_valid(self, form):
        # application_id = self.request.POST.get('application')
        application = get_object_or_404(Application, pk=self.kwargs['pk'])
        instance = form.save(commit=False)
        instance.application = application
        instance.save()
        # self.content = self.generate_description(form.cleaned_data)
        form.instance.content = self.generate_description(form.cleaned_data)
        return super().form_valid(form)

    def generate_description(self, form_data):
        templates = {'vacation':"Pareigos\nPAKEISK_MANE\n\nUAB ĮMONĖ\ndirektoriui PAKEISK_MANE\n\nPRAŠYMAS DĖL ATOSTOGŲ\n\n{start_date}\n{end_date}\n\nPrašau leisti mane kasmetinių atostogų nuo {start_date} iki {end_date} imtinai. Prašau man priklausančius atostoginius išmokėti kartu su darbo užmokesčio mokėjimu.\n\nPAKEISKMANE\n",
                     'taxes': 'taxes lalsalsldf'}
        application = get_object_or_404(Application, pk=self.kwargs['pk'])
        if application.title == 'Vacation':
            template = templates['vacation']

            # full_name = f"{self.request.user.first_name} {self.request.user.last_name}"
            start_date = form_data['start_date']
            end_date = form_data['end_date']

            description = template.format(
                start_date=start_date,
                end_date=end_date
            ) # full_name=full_name,
            return description

        if application.title == 'Taxes form':
            template = templates['taxes']

            npd = form_data['npd']
            start_date = form_data['start_date']
            
            description = template.format(
                start_date=start_date,
                npd=npd
            ) # full_name=full_name,
            return description
        
        

        # print(description)
        # return description
    
    
