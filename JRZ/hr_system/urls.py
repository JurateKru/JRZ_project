from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name='about_us'),
    path('applications/', views.ApplicationListView.as_view(), name='application_list'),
    path('application/instance/<int:pk>', views.ApplicationFormView.as_view(), name='application_instance'),
    path('application/my_application/', views.UserApplicationListView.as_view(), name='user_application_instances'),
    path('application/my_application/<int:pk>', views.UserApplicationDetailView.as_view(), name='user_application_detail'),
]
