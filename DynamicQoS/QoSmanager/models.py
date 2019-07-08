from django.db import models


# Create your models here.
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


class Application(models.Model):
    name = models.CharField(max_length=45)
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE, null=True)
    business_app = models.ForeignKey(BusinessApp, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class PolicyIn(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    applications = models.ForeignKey(Application, on_delete=models.CASCADE, null=True)
