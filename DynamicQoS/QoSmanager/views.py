from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from .models import *


# Create your views here.
def index(request):
    type1 = BusinessType.objects.create(name='type1')
    BusinessApp.objects.create(name='app1', business_type=type1)
    BusinessApp.objects.create(name='Mumbai', business_type=type1)
    BusinessApp.objects.create(name='Chennai', business_type=type1)
    BusinessApp.objects.create(name='Hyderabad', business_type=type1)
    BusinessApp.objects.create(name='New Delhi', business_type=type1)

    type2 = BusinessType.objects.create(name='type2')
    BusinessApp.objects.create(name='New York', business_type=type2)
    BusinessApp.objects.create(name='San Francisco', business_type=type2)
    BusinessApp.objects.create(name='Los Angeles', business_type=type2)
    BusinessApp.objects.create(name='Chicago', business_type=type2)
    BusinessApp.objects.create(name='Seattle', business_type=type2)

    type3 = BusinessType.objects.create(name='type3')
    BusinessApp.objects.create(name='Moscow', business_type=type3)
    BusinessApp.objects.create(name='Saint Petersburg', business_type=type3)
    BusinessApp.objects.create(name='Yekaterinburg', business_type=type3)
    BusinessApp.objects.create(name='Kazan', business_type=type3)
    BusinessApp.objects.create(name='Krasnodar', business_type=type3)
    return render(request, "home.html")


def add_application(request):
    app_form = AddApplicationForm(request.POST)
    app_id = request.POST['business_app']
    a = BusinessApp.objects.get(id=app_id)
    app_name = a.name
    print(app_name)
    type_id = request.POST['business_type']
    print(BusinessType.objects.get(id=type_id))
    Application(name=app_name, business_type=BusinessType.objects.get(id=type_id), business_app=a).save()
    return HttpResponse("success")


def applications(request):
    app_form = AddApplicationForm(request.POST)
    # apps =application.objects.all()
    # print(apps)
    ctx = {'app_form': app_form}
    return render(request, 'application.html', context=ctx)


def load_applications(request):
    business_type_id = request.GET.get('business_type')
    business_apps = BusinessApp.objects.filter(business_type_id=business_type_id).order_by('name')
    return render(request, 'application_dropdown_list_options.html', {'business_apps': business_apps})
