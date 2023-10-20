from django.shortcuts import render, redirect
from products.models import (PlacedOder, 
                             PlacedeOderItem, 
                             CustomerAddress,
                             CompletedOder,
                             CompletedOderItems,
                             Cart)
from accounts.models import CustomUser
from . forms import PlacedOderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
# Create your views here.

@login_required(login_url='user_login')
def dashboard(request):
    customer_with_product_in_cart = CustomUser.objects.filter(customer_with_product_in_cart__isnull=False).distinct()
    total_placed_oder = PlacedOder.objects.all().__len__()
    total_completed_oder = CompletedOder.objects.all().__len__
    last_30_days = datetime.now() - timedelta(days=30)
    completed_oder_last_30_days = CompletedOder.objects.filter(complete_date__gte=last_30_days).count()
    context={
        "customer_with_product_in_cart":customer_with_product_in_cart,
        'total_placed_oder':total_placed_oder,
        "total_completed_oder":total_completed_oder,
        'completed_oder_last_30_days':completed_oder_last_30_days
    }
    return render(request,'admin-panel/dashboard.html', context)


@login_required(login_url='user_login')
def show_placed_oder_list(request):
    placed_oder_list = PlacedOder.objects.all()

    context={
        'placed_oder_list':placed_oder_list
    }

    return render(request, 'admin-panel/placed-oder-list.html', context)


@login_required(login_url='user_login')
def show_placed_oder_item_list(request, id):
    #getting the placed oder object by Id
    placed_oder = PlacedOder.objects.get(id=id)
    if request.method == 'POST':
        placed_oder_form = PlacedOderForm(request.POST, instance=placed_oder)
        if placed_oder_form.is_valid():
            placed_oder_form.save()
            messages.info(request, "Updated successfully")
    placed_oder_form = PlacedOderForm(instance=placed_oder)
    oder_item_list = PlacedeOderItem.objects.filter(placed_oder=placed_oder)

    if hasattr(placed_oder, 'redirect_adter_completion'):
        placed_oder.delete()
        return redirect('show_placed_oder_list')
    
    context ={
        "oder_item_list":oder_item_list,
        'placed_oder':placed_oder,
        'placed_oder_form':placed_oder_form,
        'order_number': placed_oder.order_number
    }

    return render(request,'admin-panel/placed-oder-item-details.html', context)

@login_required(login_url='user_login')
def show_completed_oder_list(request):
    completed_oder_list = CompletedOder.objects.all()

    context={
        'completed_oder_list':completed_oder_list
    }

    return render(request, 'admin-panel/completed_oder_list.html', context)

@login_required(login_url='user_login')
def show_completed_oder_item_list(request, id):
    #getting the placed oder object by Id
    completed_oder = CompletedOder.objects.get(id=id)
    # if request.method == 'POST':
    #     placed_oder_form = PlacedOderForm(request.POST, instance=completed_oder)
    #     if placed_oder_form.is_valid():
    #         placed_oder_form.save()
    #         messages.info(request, "Updated successfully")
    # placed_oder_form = PlacedOderForm(instance=completed_oder)
    oder_item_list = CompletedOderItems.objects.filter(completed_oder=completed_oder)   
    context ={
        "oder_item_list":oder_item_list,
        'completed_oder':completed_oder,
        'order_number': completed_oder.oder_number
    }

    return render(request,'admin-panel/completed-oder-item-details.html', context)