from django import forms
from products.models import Product
from .models import VendorStore


class ProductModelAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []

    def __init__(self, *args, **kwargs):
            super(ProductModelAdminForm, self).__init__(*args, **kwargs)
            user = getattr(self, 'user', None)
            if user and user.is_authenticated:
                self.fields["vendor_stores"].queryset = VendorStore.objects.filter(
                    user=user
                )
            else:
                self.fields["vendor_stores"].queryset = VendorStore.objects.none()