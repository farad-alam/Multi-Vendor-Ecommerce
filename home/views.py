from django.shortcuts import render 
from .models import SliderArea, DisplayHotProductInCategories, PopularCategories
from products.models import Industry, Product, Categories, Cart
from django.views.decorators.csrf import csrf_exempt
from products.models import Categories
# Create your views here.


def home(request):
    sub_total = 0.00
    carts = ""
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        if carts:
            sub_total = Cart.subtotal_product_price(user=request.user)
    slider = SliderArea.objects.all()
    industry = Industry.objects.all()
    hot_products_in_cate = DisplayHotProductInCategories.objects.all()[:4]
    # vendor_user = CustomUser.objects.filter(id=6)
    trending_product = Product.objects.all()
    trending_division_title = "Trending Product"
    popular_categories = PopularCategories.objects.all()
    context = {
        "carts": carts,
        "sub_total": format(sub_total, ".2f"),
        "slider": slider,
        "industry": industry,
        "hot_products_in_cate": hot_products_in_cate,
        "trending_product": trending_product,
        "trending_division_title": trending_division_title,
        "popular_categories": popular_categories,
    }
    return render(request, "home/home.html", context)


def display_categories_post(request, id):
    categories = Categories.objects.get(id=id)
    products = Product.objects.filter(categories=categories)
    context = {"products": products}
    return render(request, "categories-post.html", context)


def test_page(request):
    return render(request, "strip/checkout.html")




def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400

# @csrf_exempt
# def create_checkout_session(request):
#     if request.method == 'POST':          
#         try:
#             data = json.loads(request.POST)
#             # Create a PaymentIntent with the order amount and currency
#             intent = stripe.PaymentIntent.create(
#                 amount=calculate_order_amount(data['items']),
#                 currency='usd',
#                 # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
#                 automatic_payment_methods={
#                     'enabled': True,
#                 },
#             )
#             return JsonResponse({
#                 'clientSecret': intent['client_secret']
#             })
            
#         except Exception as e:
#             return JsonResponse(error=str(e)), 403



