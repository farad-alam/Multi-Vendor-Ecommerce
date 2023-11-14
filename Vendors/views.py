from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.models import Group

from .models import VendorStore
from products.models import Product
# Create your views here.


def vendor_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            preview_form = form.save(commit=False)
            preview_form.user_role = 3
            # preview_form.is_staff = False
            preview_form.save()

            # get the targeted group where the user can acceess
            vendor_group = Group.objects.get(name="Vendors")

            # add user to permisssion group
            preview_form.groups.add(vendor_group)

            messages.info(request, "Your Vendor Account Created Successfully!!!!")
            return redirect("/vendor-dashboard/login/")
    else:
        form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request,'accounts/vendor/vendor_registration.html',context)