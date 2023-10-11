from django.shortcuts import render, redirect
from products.models import PlacedOder, PlacedeOderItem, CustomerAddress
from accounts.models import CustomUser
from . forms import PlacedOderForm
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def redirect_callback(placed_order_instance):
    # Check if the status is 'Order Shipped'
    if placed_order_instance.status == 'Oder Shipped':
        # Get the URL for redirection
        redirect_url = reverse('show_placed_order_list')  # Adjust the URL name accordingly
        return redirect(redirect_url)

def show_placed_oder_list(request):
    placed_oder_list = PlacedOder.objects.all()

    context={
        'placed_oder_list':placed_oder_list
    }

    return render(request, 'admin-panel/placed-oder-list.html', context)

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