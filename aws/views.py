from django.shortcuts import render
import boto3
import sys
import os
import time


# Create your views here.

def index(request):

    return render(request, 'index.html')





