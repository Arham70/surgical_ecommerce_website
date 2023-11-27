
from django import forms
from .models import CustomUser


class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'address', 'postal_code', 'country', 'telephone']
