#imports go here
import datetime  # for checking renewal date range.

from django.contrib.auth.models import User

from django import forms
from .models import Owner, FooterContent


#Classes go here
class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']  # Include other fields as necessary

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['first_name', 'last_name', 'phone_num', 'address', 'has_insurance', 'insurance_provider', 'insurance_policy_number']

    def clean(self):
        cleaned_data = super().clean()
        has_insurance = cleaned_data.get('has_insurance')
        insurance_provider = cleaned_data.get('insurance_provider')
        insurance_policy_number = cleaned_data.get('insurance_policy_number')

        # Check if has_insurance is True
        if has_insurance:
            # If insurance_provider or insurance_policy_number is empty, raise a validation error
            if not insurance_provider or not insurance_policy_number:
                raise forms.ValidationError("Insurance provider and policy number are required when insurance is selected.")

        return cleaned_data

class FooterContentForm(forms.ModelForm):
    class Meta:
        model = FooterContent
        fields = ['about_us', 'contact_email', 'contact_phone']