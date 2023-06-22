from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name='about_us'),
    path('applications/', views.ApplicationListView.as_view(), name='application_list'),
    path('application/instance/<int:pk>', views.ApplicationFormView.as_view(), name='application_instance'),
    path('export_pdf/<int:pk>', views.ExportPdfView.as_view(), name='export_pdf'),
    path('create_pdf/<int:pk>', views.render_pdf_view, name='createPDF'),
    path('application/my_application/', views.UserApplicationListView.as_view(), name='user_application_instances'),
    path('application/my_application/<int:pk>', views.UserApplicationDetailView.as_view(), name='user_application_detail'),
    path('application/department_application/', views.DepartmentApplicationListView.as_view(), name='department_application_instances'),
    path('application/department_application/<int:pk>', views.DepartmentApplicationUpdateView.as_view(), name='update_application_instance'),
]

# user_application_instances/user_instance/<int:pk>/