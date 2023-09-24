from django.shortcuts import render, redirect
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
    Cart.objects.create(user=request.user, product=product)
    return redirect("show_cart")


@login_required(login_url="user_login")
def show_cart(request):
    carts = Cart.objects.filter(user=request.user)
    context = {"carts": carts}
    return render(request, "products/cart.html", context)


@login_required(login_url="user_login")
@csrf_exempt
def increase_cart(request):
    if request.method == "POST":
        data = request.body
        data = json.loads(data)
        id = int(data['id'])
        product = Cart.objects.get(id=id)
        product.quantity += 1
        product.save()
    data = {
        "product_quantity" : product.quantity,
    }
    # return render(request, "products/cart.html", context)
    return JsonResponse(data)
