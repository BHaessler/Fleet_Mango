"""Admin configuration for the catalog app."""


from django.contrib import admin
from django.contrib.auth.models import Group  # Import Group model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

#Everything under here I added
from django import forms
from .models import Owner, VehicleType, CarMake, CarInstance, FooterContent

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

class UserOwnerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Owner.objects.update_or_create(
                user=user,
                defaults={'first_name': user.first_name, 'last_name': user.last_name}
            )
        return user

def sync_with_owner(modeladmin, request, queryset):
    for user in queryset:
        Owner.objects.update_or_create(
            user=user,
            defaults={'first_name': user.first_name, 'last_name': user.last_name}
        )
sync_with_owner.short_description = "Sync selected users with owner model"

class CustomUserAdmin(UserAdmin):
    form = UserOwnerForm
    actions = [sync_with_owner]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Only for new users
            obj.is_staff = True
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        
        if not is_superuser:
            if 'username' in form.base_fields:
                form.base_fields['username'].initial = 'default_username'
            if 'email' in form.base_fields:
                form.base_fields['email'].initial = 'default@example.com'
            if 'is_staff' in form.base_fields:
                form.base_fields['is_staff'].initial = True
            if 'first_name' in form.base_fields:
                form.base_fields['first_name'].initial = 'Default'
            if 'last_name' in form.base_fields:
                form.base_fields['last_name'].initial = 'User'
        
        return form

@admin.register(FooterContent)
class FooterContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'about_us', 'contact_email', 'contact_phone')
    # Optionally, you can customize other settings like search_fields or list_filter

    def has_add_permission(self, request):
        # Allow only one FooterContent entry
        return not FooterContent.objects.exists()

    def has_change_permission(self, request, obj=None):
        # Allow changes to the existing FooterContent
        return True

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the FooterContent
        return False

# Register the admin class with the associated model
admin.site.register(Owner, OwnerAdmin)
admin.site.register(VehicleType, VehicleTypeAdmin)
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarInstance, CarInstanceAdmin)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
