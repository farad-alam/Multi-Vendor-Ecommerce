from django.shortcuts import render, redirect, HttpResponseRedirect
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import (Product, Industry, Cart, 
                     CustomerAddress, PlacedOder, 
                     PlacedeOderItem, CuponCodeGenaration, ProductStarRatingAndReview)
from . forms import CustomerAddressForm
import json
from accounts.models import CustomUser

# Create your views here.


def product_details(request, slug):
    product = Product.objects.get(slug=slug)
    industry = Industry.objects.all()
    product_reviews = ProductStarRatingAndReview.objects.filter(product=product)
    context = {"product": product, "industry": industry,'product_reviews':product_reviews}
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
    industry = Industry.objects.all()
    sub_total = 0.00
    if carts:
        sub_total = Cart.subtotal_product_price(user=request.user)
    context = {
        "carts": carts,
        "sub_total": format(sub_total, '.2f'),
        'industry':industry
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




# @login_required(login_url="user_login")
# def check_out(request):
#     user_cart = Cart.objects.filter(user=request.user)
#     all_shipping_address = CustomerAddress.objects.filter(user=request.user)
#     selected_shipping_address = CustomerAddress.objects.filter(user=request.user).last()
#     if user_cart:
#         industry = Industry.objects.all()
#         existing_address = CustomerAddress.objects.filter(user=request.user)
#         address_form = None
#         if request.method == 'POST':
#             user = request.user
#             if not existing_address.exists():
#                 address_form = CustomerAddressForm(data=request.POST)
#                 if address_form.is_valid():
#                     shipping_address = address_form.save(commit=False)
#                     shipping_address.user = user
#                     shipping_address.save()
#                     # print(shipping_address)
#             else:         
#                 shipping_address =  existing_address[0]
#                 address_form = CustomerAddressForm(data=request.POST)
#                 if address_form.is_valid():
#                         # getting addres raw data               
#                         city = address_form.cleaned_data['city']
#                         state = address_form.cleaned_data['state']
#                         zip_code = address_form.cleaned_data['zip_code']
#                         street_address = address_form.cleaned_data['street_address']
#                         mobile = address_form.cleaned_data['mobile']
#                         # saving Shipping address
#                         shipping_address.city = city
#                         shipping_address.state = state
#                         shipping_address.zip_code = zip_code
#                         shipping_address.street_address = street_address
#                         shipping_address.mobile = mobile
#                         shipping_address.save()

#             carts = Cart.objects.filter(user=user)
#             if carts.exists():
#                 place_order = PlacedOder.objects.create(
#                     user=user,
#                     shipping_address= shipping_address,
#                     sub_total_price = Cart.subtotal_product_price(user=user)
#                 )
#                 print(place_order)
#                 print("ITS IDDDDDDDD",place_order.id)
#                 # getting the all product of user Cart and save them to PlacedOderItem then remove from Cart
#                 for item in carts:
#                     # decrese product number from Product Model
#                     product_obj = Product.objects.get(id=item.product.id)
#                     if not item.product.out_of_stoc:
#                         if product_obj.stoc >= item.quantity:
#                             product_obj.stoc = product_obj.stoc - item.quantity
#                             if product_obj.stoc == 0:
#                                 product_obj.out_of_stoc = True
#                             product_obj.save()
#                         else:
#                             shipping_address.delete()
#                             # PlacedOder.objects.get(id=place_order.id).delete()
#                             messages.info(request,f"{product_obj.title[:20]} is avilable less than your quantity")
#                             return redirect('show_cart')
#                     else:
#                         shipping_address.delete()
#                         PlacedOder.objects.get(id=place_order.id).delete()
#                         messages.info(request,f"{product_obj.title[:20]} is currently out of stock")
#                         return redirect('show_cart')           
                    
#                     PlacedeOderItem.objects.create(
#                         placed_oder=place_order,
#                         product=item.product,
#                         quantity=item.quantity,
#                         total_price=item.total_product_price
#                     )
#                     item.delete()

#                 place_order.save()
#             messages.success(request, 'Your Order Placed SuccessFully!!!')
#             return redirect('user_dashboard')
            
#         # Removing Cupon Code
#         data = request.GET.get('remove_cupon')
#         carts = Cart.objects.filter(user=request.user)
#         if data: 
#             for item in carts:
#                 item.cupon_applaied = False
#                 item.cupon_code = None
#                 item.save()

#         cupon = False
#         if carts and carts[0].cupon_applaied:
#             cupon = True

#         #Calculate the subtotal after Removing the cupon code
#         sub_total = Cart.subtotal_product_price(user=request.user)

#         #checking the existing address and retur it to the template as form
#         if existing_address.exists():
#             address_form  = CustomerAddressForm(instance=existing_address[0])
#         else:       
#             address_form = CustomerAddressForm()

#         context ={'address_form':address_form,'cupon':cupon,'carts':carts,
#                 'sub_total':sub_total,
#                 'industry':industry,
#                 'all_shipping_address':all_shipping_address,
#                 'selected_shipping_address':selected_shipping_address
#                 }
#         return render(request,'products/checkout.html',context)
#     else:
#         messages.info(request,'You have no product in your Cart')
#         return redirect('home')




@login_required(login_url="user_login")
def check_out(request):
    user_cart = Cart.objects.filter(user=request.user)
    all_shipping_address = CustomerAddress.objects.filter(user=request.user)
    user_shipping_address = CustomerAddress.objects.filter(user=request.user)
    first_cart_item = user_cart.first()
    
    if user_shipping_address and first_cart_item.shipping_address:
        selected_shipping_address = first_cart_item.shipping_address
        #saveing the address to the first cart item
        # user_cart[0].shipping_address = selected_shipping_address
        # user_cart.save()
    elif user_shipping_address:
        selected_shipping_address = user_shipping_address.last()
        #saveing the address to the first cart item
        first_cart_item.shipping_address = selected_shipping_address
        first_cart_item.save()
    else:
        selected_shipping_address = None
    
    if user_cart:
        industry = Industry.objects.all()
        if request.method == 'POST':
            selected_shipping_address_id = request.POST.get('selected_address_id')
            selected_shipping_address = CustomerAddress.objects.get(id=selected_shipping_address_id)
            #saveing the address to the first cart item
            first_cart_item = user_cart.first()
            first_cart_item.shipping_address = selected_shipping_address
            first_cart_item.save()

        # Removing Cupon Code
        data = request.GET.get('remove_cupon')
        if data: 
            for item in user_cart:
                item.cupon_applaied = False
                item.cupon_code = None
                item.save()

        cupon = False
        if user_cart and user_cart[0].cupon_applaied:
            cupon = True

        #Calculate the subtotal after Removing the cupon code
        sub_total = Cart.subtotal_product_price(user=request.user)

        #checking the existing address and retur it to the template as form      
        address_form = CustomerAddressForm()

        context ={'address_form':address_form,'cupon':cupon,'carts':user_cart,
                'sub_total':sub_total,
                'industry':industry,
                'all_shipping_address':all_shipping_address,
                'selected_shipping_address':selected_shipping_address
                }
        return render(request,'products/checkout.html',context)
    else:
        messages.info(request,'You have no product in your Cart')
        return redirect('home')



@login_required(login_url="user_login")
def placed_oder(request):

    #getting the user cart
    user_cart = Cart.objects.filter(user=request.user)
    sub_total_price = Cart.subtotal_product_price(request.user)

    # Creting new PlacedOder for adding in it PlacedOderItem
    user_placedOder = PlacedOder.objects.create(
        user=request.user,
        shipping_address = user_cart.first().shipping_address,
        sub_total_price = sub_total_price,
        paid = True
    )
    user_placedOder.save()

    # Itarate the user_cart and add this item to the PladeOderIteam

    for item in user_cart:
        PlacedeOderItem.objects.create(
            placed_oder=user_placedOder,
            product = item.product,
            quantity = item.quantity,
            total_price = item.total_product_price
        )
        item.delete()

    messages.success(request,'Oder Placed Succesfully')

    return user_placedOder


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


def add_product_review_and_rating(request):
    if request.user.is_authenticated and request.user.user_role == '1':
        if request.method == 'POST':
            data = request.body
            data = json.loads(data)
            product_id = int(data.get('product_id'))
            stars = data.get('stars')
            review_messages = data.get('review_messages')

            # Geting the Product and User obj
            product_obj = Product.objects.get(id=product_id)
            user_obj = CustomUser.objects.get(id=request.user.id)
            if user_obj.user_role == '1':                   
                # Creting New Product Review
                product_review_instance = ProductStarRatingAndReview(
                    product=product_obj, user=user_obj, stars=stars, review_message=review_messages
                )
                product_review_instance.save()

                return JsonResponse({"status":200})
    else:
        messages.info(request,f"{request.user.first_name} is not a customer!!!")
        # print(request.META)
        current_page_url = request.META.get('HTTP_REFERER')
        print(current_page_url)
        # return product_details(request,current_page_url)
        return redirect('/')


# SRTIPE PAYMENTS VIEWS ---------------------->>

def save_shipping_address(request):
    if request.method == 'POST':
        new_address = CustomerAddressForm(data=request.POST)
        if new_address.is_valid():
            temp_new_address = new_address.save(commit=False)
            temp_new_address.user = request.user
            temp_new_address.save()
            user_cart = Cart.objects.filter(user=request.user)
            first_cart_item = user_cart.first()
            first_cart_item.shipping_address = temp_new_address
            first_cart_item.save()
    return redirect('check_out')