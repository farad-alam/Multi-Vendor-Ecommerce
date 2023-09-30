from django.shortcuts import render, redirect
from . models import CustomUser
from .forms import RegistrationForm
from products.models import PlacedOder
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def registration_view(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your account created successfully!!!')
            return redirect('registration_view')
    else:
        form = RegistrationForm()
    context = {
        'form':form
    }
    return render(request,'accounts/user/registration.html', context)

def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=email,password=password)
            if user is not None:
                login(request, user)
            return redirect('user_profile')
    else:
        login_form = AuthenticationForm()
    context={
            'login_form':login_form
        }

    return render(request,'accounts/user/login.html',context)

@login_required(login_url='user_login')
def user_profile(request):
    placed_oders = PlacedOder.objects.filter(user=request.user)
    if placed_oders:
        print(placed_oders)
        print(placed_oders[0])
        placed_oders = placed_oders[0].order_items.all()
    else:
        placed_oders = None
    context = {
        'placed_oders':placed_oders
    }
    return render(request,'accounts/user/user-profile.html', context)

@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    return redirect('home')