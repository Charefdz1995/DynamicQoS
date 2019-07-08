from django.urls import path

from QoSmanager import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/load-applications/', views.load_applications, name='ajax_load_applications'),
    path('applications/', views.applications, name='applications'),
    path('add_application/', views.add_application, name='add_application'),
]
