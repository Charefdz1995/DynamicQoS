from django.urls import path

from QoSmanager import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/load-applications/', views.load_applications, name='ajax_load_applications'),
    path('applications/<police_id>', views.applications, name='applications'),
    path('add_application/<police_id>', views.add_application, name='add_application'),
    path('policies/', views.policies, name='policies'),
    path('add_policy/', views.add_policy, name='add_policy'),
]
