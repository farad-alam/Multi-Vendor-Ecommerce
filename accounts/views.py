from django.shortcuts import render, redirect
from . models import CustomUser
from .forms import RegistrationForm, CustomUserEditForm
from products.models import PlacedOder, CompletedOder
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
            return redirect('user_login')
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
            return redirect('user_dashboard')
    else:
        login_form = AuthenticationForm()
    context={
            'login_form':login_form
        }

    return render(request,'accounts/user/login.html',context)



@login_required(login_url='user_login')
def user_dashboard(request):
    placed_oders_by_oder_id = PlacedOder.placed_oders_by_user(user=request.user)
    # print(placed_oders_by_oder_id)
    placede_oder_obj = PlacedOder.objects.filter(user=request.user)
    if placede_oder_obj:
        shipping_addess = placede_oder_obj[0].shipping_address
    else:
        shipping_addess = None
    
    completed_order= CompletedOder.objects.filter(user=request.user)

    context = {
        'placed_oders_by_oder_id':placed_oders_by_oder_id,
        "shipping_addesss":shipping_addess,
        "completed_order":completed_order,
    }
    return render(request,'accounts/user/user-dashboard.html', context)

@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='user_login')
def user_profile(request):
    
    return render(request, 'accounts/user/user-profile.html')

@login_required(login_url='user_login')
def user_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # Change 'profile' to the appropriate redirect URL
    else:
        form = CustomUserEditForm(instance=request.user)

    context={
        "form":form
    }
    
    return render(request, 'accounts/user/user-profile.html', context)
