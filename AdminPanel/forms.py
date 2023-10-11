from django import forms
from products.models import PlacedOder, CustomerAddress


class PlacedOderForm(forms.ModelForm):

    class Meta:
        model = PlacedOder
        fields = ['order_number','sub_total_price', 'paid', 'status']
        widgets = {
        'sub_total_price': forms.NumberInput(attrs={'class': 'form-control','readonly': 'readonly'}),
        'status': forms.Select(attrs={'class': 'form-control'}),
        # 'shipping_address': forms.Select(attrs={'class': 'form-control','readonly': 'readonly'}),
        'paid': forms.CheckboxInput(attrs={'class': ''}),
        'order_number': forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
    }
        
    
