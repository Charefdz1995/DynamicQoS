from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import *


# Create your views here.
def index(request):
    input_p = PolicyIn.objects.create(name='input')
    out_o = PolicyOut.objects.create(name='output')
    policing1 = Policing.objects.create(cir='1', pir='5', dscp_transmit='af11')
    policing2 = Policing.objects.create(cir='1', pir='5', dscp_transmit='af11')
    policing3 = Policing.objects.create(cir='1', pir='5', dscp_transmit='af11')
    policing4 = Policing.objects.create(cir='1', pir='5', dscp_transmit='af11')
    class1 = RegroupementClass.objects.create(name="class1", policy_out=out_o, policing=policing1, bandwidth="100")
    class2 = RegroupementClass.objects.create(name="class2", policy_out=out_o, policing=policing2, bandwidth="100")
    class3 = RegroupementClass.objects.create(name="class3", policy_out=out_o, policing=policing3, bandwidth="100")
    class4 = RegroupementClass.objects.create(name="class4", policy_out=out_o, policing=policing4, bandwidth="100")
    af41 = Dscp.objects.create(priority='4', drop_prob='1', regroupement_class=class1, drop_min='1', drop_max='5',
                               denominator='2')
    af31 = Dscp.objects.create(priority='3', drop_prob='1', regroupement_class=class2, drop_min='1', drop_max='5',
                               denominator='2')
    af21 = Dscp.objects.create(priority='2', drop_prob='1', regroupement_class=class3, drop_min='1', drop_max='5',
                               denominator='2')
    af11 = Dscp.objects.create(priority='1', drop_prob='1', regroupement_class=class4, drop_min='1', drop_max='5',
                               denominator='2')
    Application.objects.create(name="app1", dscp_value="af41", policy_in=input_p, regroupement_class=class1, dscp=af41)
    Application.objects.create(name="app2", dscp_value="af31", policy_in=input_p, regroupement_class=class2, dscp=af31)
    Application.objects.create(name="app3", dscp_value="af21", policy_in=input_p, regroupement_class=class3, dscp=af21)
    Application.objects.create(name="app4", dscp_value="af11", policy_in=input_p, regroupement_class=class4, dscp=af11)
    print(out_o.render_policy)
    # police = BusinessType.objects.create(name='voice')
    # BusinessApp.objects.create(name='rtp', business_type=police)
    # BusinessApp.objects.create(name='voip', business_type=police)
    # policee = BusinessType.objects.create(name='django')
    # BusinessApp.objects.create(name='rtp2', business_type=policee)
    # BusinessApp.objects.create(name='voip2', business_type=policee)
    # rend = police.render_policy
    # print(rend)

    return HttpResponse("success")


def add_application(request, police_id):
    # app_form = AddApplicationForm(request.POST)
    app_id = request.POST['business_app']
    a = BusinessApp.objects.get(id=app_id)
    app_name = a.name
    print(app_name)
    type_id = request.POST['business_type']
    print(BusinessType.objects.get(id=type_id))
    Application(policy_in_id=police_id, drop_prob=request.POST['drop_prob'], app_priority=request.POST['app_priority'],
                name=app_name,
                business_type=BusinessType.objects.get(id=type_id), business_app=a).save()
    return HttpResponse("success")


def applications(request, police_id):
    app_form = AddApplicationForm(request.POST)
    # apps =application.objects.all()
    # print(apps)
    ctx = {'app_form': app_form, 'police_id': police_id}
    return render(request, 'application.html', context=ctx)


def add_input_policy(request):
    # policy_form = AddInputPolicyForm(request.POST)
    a = PolicyIn(name=request.POST['name'], description=request.POST['description'])
    a.save()
    police_id = a.id
    return redirect('applications', police_id=police_id)


def input_policies(request):
    policy_form = AddInputPolicyForm(request.POST)
    ctx = {'policy_form': policy_form}
    return render(request, 'policy.html', context=ctx)


def load_applications(request):
    business_type_id = request.GET.get('business_type')
    business_apps = BusinessApp.objects.filter(business_type_id=business_type_id).order_by('name')
    return render(request, 'application_dropdown_list_options.html', {'business_apps': business_apps})
