from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Industry, Cart
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
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
    context = {"carts": carts}
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
            carts_product = Cart.objects.filter(user=request.user)
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
            


    # print(carts_product[0].product.productimage_set.first().image)
    data = {
        "product_quantity" : product.quantity,
        "total_product_price": product.total_product_price,
        "carts_product": products_list
    }
    # return render(request, "products/cart.html", context)
    return JsonResponse(data)
