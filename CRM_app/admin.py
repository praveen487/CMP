from django.contrib import admin
from .models import *
#
# Username = PMV
# password = Password@123
#

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)
