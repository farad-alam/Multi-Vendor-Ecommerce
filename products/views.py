from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import (Product, Industry, Cart, 
                     CustomerAddress, PlacedOder, 
                     PlacedeOderItem, CuponCodeGenaration)
from . forms import CustomerAddressForm
import json


# Create your views here.


def product_details(request, slug):
    product = Product.objects.get(slug=slug)
    industry = Industry.objects.all()

    context = {"product": product, "industry": industry}
    return render(request, "products/product-details.html", context)


@login_required(login_url="user_login")
def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    if not Cart.objects.filter(Q(user=request.user) & Q(product=product)).exists():
        Cart.objects.create(user=request.user, product=product)
        return redirect("show_cart")
    return redirect('show_cart')


@login_required(login_url="user_login")
def show_cart(request):
    carts = Cart.objects.filter(user=request.user)
    sub_total = 0.00
    if carts:
        sub_total = Cart.subtotal_product_price(user=request.user)
    context = {
        "carts": carts,
        "sub_total": format(sub_total, '.2f')
        }
    return render(request, "products/cart.html", context)


@login_required(login_url="user_login")
@csrf_exempt
def increase_cart(request):
    products_list  = []

    if request.method == "POST":
        data = request.body
        data = json.loads(data)
        id = int(data['id'])
        values = int(data['values'])

        carts_product = Cart.objects.filter(user=request.user)
        product = Cart.objects.get(id=id)

        #increse quantity
        if values == 1 and product.quantity < 50:                
            product.quantity += 1
            product.save()
        #Decrese quantity
        elif values == 2 and product.quantity > 1:
            product.quantity -= 1
            product.save()
        #remove product
        elif values == 0:
            product.delete()
            if carts_product != None:
                for product in carts_product:
                    product_details_dict = {}
                    id = product.product.id
                    image = product.product.productimage_set.first().image
                    title = product.product.title
                    discounted_price = product.product.discounted_price
                    total_product_price = product.total_product_price
                    quantity = product.quantity
                    product_details_dict['id'] = id
                    product_details_dict['title'] = title
                    product_details_dict['quantity'] = quantity
                    product_details_dict['regular_price'] = discounted_price
                    product_details_dict['total_product_price'] = total_product_price
                    product_details_dict['image'] = image
                    products_list.append(product_details_dict)
            else:
                products_list.append('no-product')

    sub_total = Cart.subtotal_product_price(user=request.user)
    print(format(product.total_product_price, ".2f"))
    data = {
        "product_quantity" : product.quantity,
        "total_product_price": product.total_product_price,
        'sub_total': sub_total,
        "carts_product": products_list,

    }
    return JsonResponse(data)

@login_required(login_url="user_login")
def check_out(request):
    existing_address = CustomerAddress.objects.filter(user=request.user)
    if request.method == 'POST':
        user = request.user
        if not existing_address.exists():
            address_form = CustomerAddressForm(data=request.POST)
            if address_form.is_valid():
                shipping_address = address_form.save(commit=False)
                shipping_address.user = user
                shipping_address.save()
                print(shipping_address)

        carts = Cart.objects.filter(user=user)
        if carts.exists():
            place_order = PlacedOder.objects.create(
                user=user,
                shipping_address=existing_address[0],
                sub_total_price = Cart.subtotal_product_price(user=user)
            )
            # getting the all product of user Cart and save them to PlacedOderItem then remove from Cart
            for item in carts:
                PlacedeOderItem.objects.create(
                    placed_oder=place_order,
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.total_product_price
                )
                item.delete()
            place_order.save()
        messages.success(request, 'Your Order Placed SuccessFully!!!')
        return redirect('user_profile')
        
    # Removing Cupon Code
    data = request.GET.get('remove_cupon')
    carts = Cart.objects.filter(user=request.user)
    if data: 
        for item in carts:
            item.cupon_applaied = False
            item.cupon_code = None
            item.save()
    cupon = False
    if carts and carts[0].cupon_applaied:
        cupon = True
    #Calculate the subtotal after Removing the cupon code
    sub_total = Cart.subtotal_product_price(user=request.user)
    #checking the existing address and retur it to the template as form
    if existing_address.exists():
        address_form  = CustomerAddressForm(instance=existing_address[0])
    else:       
        address_form = CustomerAddressForm()
    # address_form = CustomerAddressForm()
    context ={'address_form':address_form,'cupon':cupon,'carts':carts,'sub_total':sub_total}
    return render(request,'products/checkout.html',context)


def placed_oder(request):

    context ={

    }
    return render(request, 'accounts/user/user-profile.html',context)

@login_required(login_url="user_login")
def cupon_apply(request):
    if request.method =='POST':
        cupon_code = request.POST.get('cupon_code')
        print(cupon_code)
        cupon_obj = CuponCodeGenaration.objects.filter(cupon_code=cupon_code)
        if cupon_obj.exists():
            less_ammount_by_cupon = (Cart.subtotal_product_price(user=request.user)*cupon_obj[0].discoun_parcent)/100
            # checking Limit of discounted ammount
            user_carts = Cart.objects.filter(user=request.user)
            if less_ammount_by_cupon <= cupon_obj[0].up_to or less_ammount_by_cupon > cupon_obj[0].up_to:
                for item in user_carts:
                    item.cupon_code = CuponCodeGenaration.objects.get(cupon_code=cupon_code)
                    item.cupon_applaied = True
                    item.save()         
    return redirect('check_out')



