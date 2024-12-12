from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'customer_surname', 'phone_number', 'customer_email']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'customer_surname': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'customer_phone_number': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
        }