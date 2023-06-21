from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name='about_us'),
    path('applications/', views.ApplicationListView.as_view(), name='application_list'),
    path('application/instance/<int:pk>', views.ApplicationFormView.as_view(), name='application_instance'),
    path('export_pdf', views.export_pdf, name='export_pdf'),
    path('create_pdf', views.render_pdf_view, name='createPDF'),
]

# user_application_instances/user_instance/<int:pk>/