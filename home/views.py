from django.shortcuts import render
from . models import SliderArea, DisplayHotProductInCategories
from products.models import Industry, Product
# Create your views here.

def home(request):
    slider = SliderArea.objects.all()
    industry = Industry.objects.all()
    hot_products_in_cate = DisplayHotProductInCategories.objects.all()[:4]
    trending_product = Product.objects.all()
    trending_division_title = 'Trending Product'
    context = {
        'slider':slider,
        'industry':industry,
        'hot_products_in_cate':hot_products_in_cate,
        'trending_product':trending_product,
        'trending_division_title':trending_division_title

    }
    return render(request,'home/home.html', context)