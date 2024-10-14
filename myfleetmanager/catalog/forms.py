#imports go here
import datetime  # for checking renewal date range.

from django.contrib.auth.models import User, Group

from django import forms
from .models import Owner, FooterContent


#Classes go here
class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']  # Include other fields as necessary

class UserManagementForm(forms.ModelForm):
    password = forms.CharField(
        required=False,  # Make this field optional
        widget=forms.PasswordInput,
    )
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        empty_label="Select a group",
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'groups']  # Include groups in the fields

    def save(self, commit=True):
        user = super().save(commit=False)
        # Check if the password field is not empty
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Only set if a new password is provided
        if commit:
            user.save()
        # Assign the user to the selected group(s)
        # Ensure we pass a list to the set() method
            if self.cleaned_data['groups']:
                user.groups.set([self.cleaned_data['groups']])  # Wrap in a list
            else:
                user.groups.clear()  # Clear groups if none selected
        return user

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