from django.contrib import admin
#Everything under here I added
from .models import Owner, VehicleType, CarMake, CarInstance
# Register your models here.
admin.site.register(CarMake)
admin.site.register(Owner)
admin.site.register(VehicleType)
admin.site.register(CarInstance)