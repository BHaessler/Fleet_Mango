"""Admin configuration for the catalog app."""


from django.contrib import admin
#Everything under here I added
from .models import Owner, VehicleType, CarMake, CarInstance

# Register your models here.
# admin.site.register(CarMake)
# admin.site.register(Owner)
# admin.site.register(VehicleType)
# admin.site.register(CarInstance)

# Define the admin class
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name")

class VehicleTypeAdmin(admin.ModelAdmin):
    pass

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("manuName", "carModel", "vehicleType")

class CarInstanceAdmin(admin.ModelAdmin):
    list_display = ("car", "license_plate", "mechanic_stat", "color", "modelYear", "owner")
    list_filter = ("modelYear", "status")

    fieldsets = (
        (None, {
            'fields': ("car", "license_plate", "color", "modelYear", "owner")
        }),
        ("Availability",{
            "fields":("status", "due_back", "mechanic_stat")
        })
    )

# Register the admin class with the associated model
admin.site.register(Owner, OwnerAdmin)
admin.site.register(VehicleType, VehicleTypeAdmin)
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarInstance, CarInstanceAdmin)

