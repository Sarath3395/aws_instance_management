from django.urls import path
from . import views

urlpatterns = [
    path('stop',views.stop, name='register'),
    path('start',views.start, name='start'),
    path('regioninstances',views.regioninstances, name='regioninstances'),


]