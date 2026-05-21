from django import forms
from .models import Service,ServiceCategory

class addServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter service name'
            }),
            'desc': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
             'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the price'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                
            }),
        }