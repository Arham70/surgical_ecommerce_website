
from django import forms
from .models import CustomUser
from .models import RequestProductForm


class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'address', 'postal_code', 'country', 'telephone']


class ProductForm(forms.ModelForm):
    class Meta:
        model = RequestProductForm
        fields = ['name', 'email', 'phoneNo', 'address', 'companyName', 'productName', 'detail']


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='Email')