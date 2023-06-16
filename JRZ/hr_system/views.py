from django.shortcuts import render
from django.views import generic
from . models import Application
from django.db.models import Q

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