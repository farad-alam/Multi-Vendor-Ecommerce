from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm
from django.contrib import messages
from .models import VendorStore
from products.models import Product
# Create your views here.

def vendor_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            preview_form = form.save(commit=False)
            preview_form.user_role = 3
            preview_form.save()
            messages.info(request,'Your Vendor Account Created Successfully!!!!')
            return redirect('/vendor-dashboard/login/')
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request,'accounts/vendor/vendor_registration.html',context)

def vendor_store_with_product(request, store_id):
    vendor_store_obj = VendorStore.objects.get(id=store_id)
    vendor_store_products = Product.objects.filter(vendor_stores = vendor_store_obj)
    context = {
        'vendor_store_products':vendor_store_products,
        'vendor_store_obj':vendor_store_obj
    }
    return render(request,'accounts/vendor/vendor_store_with_product.html', context)