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

class ApplicationFormView(generic.CreateView):
    model = ApplicationInstance
    form_class = ApplicationInstanceForm
    template_name = 'hr_system/vacation.html'
    success_url = reverse_lazy('application_list')

    def get_initial(self):
        initial = super().get_initial()
        obj = get_object_or_404(Application, pk=self.kwargs['pk'])
        initial['content'] = obj.description
        return initial
    
    
