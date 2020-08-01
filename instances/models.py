from django.db import models

# Create your models here.

class c4cxlargetable(models.Model):

    date = models.CharField(max_length=250)
    time = models.CharField(max_length=250)
    price = models.CharField(max_length=250)

class instance_creation(models.Model):

    terminated_id = models.CharField(max_length=250)
    creation_id = models.CharField(max_length=250)

class ami_creation(models.Model):

    instance_id = models.CharField(max_length=250)
    ami_id = models.CharField(max_length=250)

class check_spot(models.Model):

    instance_id = models.CharField(max_length=250)
    spot_indi = models.BooleanField()