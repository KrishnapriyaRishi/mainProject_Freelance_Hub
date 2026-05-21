from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

from .models import CustomerProfile,ServiceProviderProfile


class RegisterUser(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email','phone'
        ]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        # fields = ['name','email']
        exclude = ['user']


class ProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProviderProfile
        exclude = ['is_verified','average_rating','total_reviews']



