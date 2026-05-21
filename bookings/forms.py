from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['scheduled_date','address']
        widgets = {
            
		 
		'scheduled_date': 
        forms.DateInput(attrs={'type': 'date',
                'class': 'form-control',
				'id':'dateInput'
		
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
            
        }
