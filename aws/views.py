from django.shortcuts import render
from .models import  c4cxlargetable
import boto3
import sys
import os
import time


# Create your views here.

def index(request):
    c4 = c4cxlargetable.objects.all()
    return render(request, 'index.html', {'c4': c4})





