import json

import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import *
from .models import *


# Create your views here.
def index(request):

    topo = Topology.objects.create(topology_name="test", topology_desc="test")
    device = Device.objects.create(hostname="router1", topology_ref=topo)
    int1 = Interface.objects.create(interface_name="g0/0", device_ref=device,ingress=True)
    int2 = Interface.objects.create(interface_name="g1/0", device_ref=device, ingress=True)
    int3 = Interface.objects.create(interface_name="g2/0", device_ref=device, ingress=False)
    int4 = Interface.objects.create(interface_name="g3/0", device_ref=device, ingress=False)

    # url = "http://192.168.0.128:8080/qosapi/topologies"
    # r = requests.get(url)
    #
    # topo = (r.json())
    # # print(type(topo))
    # print(topo['topologies'])
    # for topolo in topo['topologies']:
    #     top = Topology.objects.create(topology_name=topolo['topology_name'], topology_desc=topolo['topology_desc'])
    #     devices = topolo['devices']
    #     for device in devices:
    #         man = device['management']
    #         mana = Access.objects.create(management_interface=man['management_interface'],
    #                                      management_address=['management_address'],
    #                                      username=['username'],
    #                                      password=['password'])
    #         dev = Device.objects.create(hostname=device['hostname'], topology_ref=top,management=mana)
    #         interfaces = device['interfaces']
    #         for interface in interfaces:
    #             Interface.objects.create(device_ref=dev,
    #                                      interface_name=interface['interface_name'],
    #                                      ingress=interface['ingress'])
    #
    # interfaces=Interface.objects.all()
    # for i in interfaces:
    #     print(i.device_ref)

        #print(devices)
    # for device in topo['topologies']:
    #     Device.objects.create(hostname=device['hostname'])

    # json_url = urlopen(url)
    #
    # data = json.loads(json_url)
    #
    # print(data)
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

    return HttpResponse('ssssss')


def add_application(request, police_id):
    # app_form = AddApplicationForm(request.POST)
    app_id = request.POST['business_app']
    type_id = request.POST['business_type']
    groupe = Group.objects.get(priority=request.POST['app_priority'], policy_id=police_id)

    Application(policy_in_id=PolicyIn.objects.get(policy_ref_id=police_id).id,
                drop_prob=request.POST['drop_prob'],
                app_priority=request.POST['app_priority'],
                business_type=BusinessType.objects.get(id=type_id),
                business_app=BusinessApp.objects.get(id=app_id),
                group=groupe,
                source=request.POST['source'],
                destination=request.POST['destination'],
                begin_time=request.POST['begin_time'],
                end_time=request.POST['end_time'],).save()
    return redirect('applications', police_id=police_id)


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
    PolicyIn.objects.create(policy_ref=a)
    interfaces = Interface.objects.filter(ingress=False)
    Group.objects.create(name="business", priority="4", policy=a)
    Group.objects.create(name="critical", priority="3", policy=a)
    Group.objects.create(name="non-business", priority="2", policy=a)
    Group.objects.create(name="non-business2", priority="1", policy=a)
    for interface in interfaces:
        po = PolicyOut.objects.create(policy_ref=a)
        interface.policy_out_ref = po
        interface.save()
        RegroupementClass.objects.create(group=Group.objects.get(priority="4", policy=a),
                                         policy_out=po)
        RegroupementClass.objects.create(group=Group.objects.get(priority="3", policy=a),
                                         policy_out=po)
        RegroupementClass.objects.create(group=Group.objects.get(priority="2", policy=a),
                                         policy_out=po)
        RegroupementClass.objects.create(group=Group.objects.get(priority="1", policy=a),
                                         policy_out=po)

    return redirect('applications', police_id=police_id)


def policies(request):
    policy_form = AddPolicyForm(request.POST)
    ctx = {'policy_form': policy_form}
    return render(request, 'policy.html', context=ctx)


def load_applications(request):
    business_type_id = request.GET.get('business_type')
    business_apps = BusinessApp.objects.filter(business_type_id=business_type_id).order_by('name')
    return render(request, 'application_dropdown_list_options.html', {'business_apps': business_apps})
