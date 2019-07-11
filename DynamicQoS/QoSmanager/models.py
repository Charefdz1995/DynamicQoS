from django.db import models

# Create your models here.
from jinja2 import Environment, FileSystemLoader

from DynamicQoS.settings import NET_CONF_TEMPLATES

import napalm


class BusinessType(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class BusinessApp(models.Model):
    name = models.CharField(max_length=45)
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE, null=True)
    match = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class Policy(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)


class PolicyIn(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    policy_ref = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    @property
    def render_policy(self):
        env = Environment(loader=FileSystemLoader(NET_CONF_TEMPLATES))
        classes = Application.objects.filter(policy_in_id=self.id)
        named = env.get_template("policyIn.j2")
        config_file = named.render(classes=classes, a=self)
        confige = config_file.splitlines()
        print(confige)
        driver = napalm.get_network_driver('ios')
        device = driver(hostname='192.168.5.1', username='admin',
                        password='admin')

        print('Opening ...')
        device.open()
        print('Loading replacement candidate ...')
        device.load_merge_candidate(config=config_file)
        print('\nDiff:')
        print(device.compare_config())
        print('Committing ...')

        return device.commit_config()


class PolicyOut(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    policy_ref = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    @property
    def render_policy(self):
        env = Environment(loader=FileSystemLoader(NET_CONF_TEMPLATES))
        regroupement_classes = RegroupementClass.objects.filter(policy_out_id=self.id)
        dscp_list = Dscp.objects.all()
        classes = Application.objects.all()
        named = env.get_template("policyOut.j2")
        config_file = named.render(classes=classes, a=self, regroupement_classes=regroupement_classes,
                                   dscp_list=dscp_list)
        return config_file


class Policing(models.Model):
    cir = models.CharField(max_length=45)
    pir = models.CharField(max_length=45)
    dscp_transmit = models.CharField(max_length=45)


class RegroupementClass(models.Model):
    name = models.CharField(max_length=45)
    policy_out = models.ForeignKey(PolicyOut, on_delete=models.CASCADE, null=True)
    policing = models.ForeignKey(Policing, on_delete=models.CASCADE, null=True)
    priority = models.CharField(max_length=45)
    bandwidth = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class Dscp(models.Model):
    regroupement_class = models.ForeignKey(RegroupementClass, on_delete=models.CASCADE, null=True)
    priority = models.CharField(max_length=45)
    drop_prob = models.CharField(max_length=45)
    drop_min = models.CharField(max_length=45)
    drop_max = models.CharField(max_length=45)
    denominator = models.CharField(max_length=45)

    @property
    def dscp_value(self):
        return "AF{}{}".format(self.priority, self.drop_prob)


class Application(models.Model):
    Low, Med, High = "1", "2", "3"
    DROP = (
        (Low, "1"),
        (Med, "2"),
        (High, "3")
    )
    Low, Med, High, Priority = "1", "2", "3", "4"
    PRIORITY = (
        (Low, "1"),
        (Med, "2"),
        (High, "3"),
        (Priority, "4")
    )

    name = models.CharField(max_length=45)
    match = models.CharField(max_length=45)
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE, null=True)
    business_app = models.ForeignKey(BusinessApp, on_delete=models.CASCADE, null=True)
    policy_in = models.ForeignKey(PolicyIn, on_delete=models.CASCADE, null=True)
    app_priority = models.CharField(max_length=20, choices=PRIORITY)
    drop_prob = models.CharField(max_length=20, choices=DROP)
    dscp_value = models.CharField(max_length=45)
    dscp = models.ForeignKey(Dscp, on_delete=models.CASCADE, null=True)
    regroupement_class = models.ForeignKey(RegroupementClass, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Topology(models.Model):
    topology_name = models.CharField(max_length=45)
    topology_desc = models.CharField(max_length=45)

    def __str__(self):
        return self.topology_name


class Access(models.Model):
    management_interface = models.CharField(max_length=45)
    management_address = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    enable_secret = models.CharField(max_length=45)


class Device(models.Model):
    hostname = models.CharField(max_length=45)
    management = models.ForeignKey(Access, on_delete=models.CASCADE, null=True)
    topology_ref = models.ForeignKey(Topology, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.hostname


class Interface(models.Model):
    interface_name = models.CharField(max_length=45)
    ingress = models.BooleanField(default=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)

