from django.shortcuts import render
from .models import  c4cxlargetable,t2micro
import boto3
import sys
import os
import time


# Create your views here.

def index(request):
    c4 = t2micro.objects.all()
    return render(request, 'index.html', {'c4': c4})


def about(request):

    return render(request, 'about.html')

