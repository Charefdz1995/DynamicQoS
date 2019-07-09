from django.urls import path

from QoSmanager import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/load-applications/', views.load_applications, name='ajax_load_applications'),
    path('applications/<police_id>', views.applications, name='applications'),
    path('add_application/<police_id>', views.add_application, name='add_application'),
    path('input_policies/', views.input_policies, name='input_policies'),
    path('add_input_policy/', views.add_input_policy, name='add_input_policy'),
]
