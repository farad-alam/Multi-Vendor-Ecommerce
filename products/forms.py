from django import forms
from .models import CustomerAddress


class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = CustomerAddress
        fields = ['state','city','zip_code','street_address','mobile']
        widgets = {
            'state': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'zip_code': forms.NumberInput(attrs={'class':'form-control'}),
            'street_address': forms.Textarea(attrs={'class':'form-control','rows':5,'cols':50}),
            'mobile': forms.NumberInput(attrs={'class':'form-control'}),
        }        