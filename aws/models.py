from django.db import models

# Create your models here.
class c4cxlargetable(models.Model):

    date = models.CharField(max_length=250)
    time = models.CharField(max_length=250)
    price = models.CharField(max_length=250)

class t2micro(models.Model):

    date = models.CharField(max_length=250)
    time = models.CharField(max_length=250)
    price = models.CharField(max_length=250)