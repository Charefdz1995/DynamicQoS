import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import *


# Create your views here.
def index(request):
    BusinessType.objects.create(name="Application")
    BusinessType.objects.create(name="application-group")
    BusinessType.objects.create(name="Category")
    BusinessType.objects.create(name="sub-category")
    BusinessType.objects.create(name="device-class")
    BusinessType.objects.create(name="media-type")
    with open("/home/djoudi/PycharmProjects/DynamicQoS/DynamicQoS/QoSmanager/nbar_application.json", 'r') as jsonfile:
        ap = json.load(jsonfile)
        for app in ap['applications']:
            bu = BusinessType.objects.get(name=app['business_type'])
            BusinessApp(name=app['name'], match=app['match'], business_type=bu).save()

    return HttpResponse("success")


def add_application(request, police_id):
    # app_form = AddApplicationForm(request.POST)
    app_id = request.POST['business_app']
    type_id = request.POST['business_type']

    Application(policy_in_id=PolicyIn.objects.get(policy_ref_id=police_id).id,
                drop_prob=request.POST['drop_prob'],
                app_priority=request.POST['app_priority'],
                business_type=BusinessType.objects.get(id=type_id),
                business_app=BusinessApp.objects.get(id=app_id)).save()
    return HttpResponse("success")


def applications(request, police_id):
    app_form = AddApplicationForm(request.POST)
    # apps =application.objects.all()
    # print(apps)
    ctx = {'app_form': app_form, 'police_id': police_id}
    return render(request, 'application.html', context=ctx)


def add_policy(request):
    # policy_form = AddInputPolicyForm(request.POST)
    a = Policy(name=request.POST['name'], description=request.POST['description'])
    a.save()
    police_id = a.id
    PolicyIn.objects.create(name=a.name , policy_ref=a)
    return redirect('applications', police_id=police_id)


def policies(request):
    policy_form = AddPolicyForm(request.POST)
    ctx = {'policy_form': policy_form}
    return render(request, 'policy.html', context=ctx)


def load_applications(request):
    business_type_id = request.GET.get('business_type')
    business_apps = BusinessApp.objects.filter(business_type_id=business_type_id).order_by('name')
    return render(request, 'application_dropdown_list_options.html', {'business_apps': business_apps})
