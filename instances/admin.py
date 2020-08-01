from django.contrib import admin
from .models import  c4cxlargetable,instance_creation,ami_creation,check_spot
# Register your models here.


admin.site.register(c4cxlargetable)
admin.site.register(instance_creation)
admin.site.register(ami_creation)
admin.site.register(check_spot)