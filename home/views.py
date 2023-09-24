from django.shortcuts import render
from . models import SliderArea, DisplayHotProductInCategories, PopularCategories
from products.models import Industry, Product, Categories
# Create your views here.

def home(request):
    slider = SliderArea.objects.all()
    industry = Industry.objects.all()
    hot_products_in_cate = DisplayHotProductInCategories.objects.all()[:4]
    trending_product = Product.objects.all()
    trending_division_title = 'Trending Product'
    popular_categories = PopularCategories.objects.all()
    context = {
        'slider':slider,
        'industry':industry,
        'hot_products_in_cate':hot_products_in_cate,
        'trending_product':trending_product,
        'trending_division_title':trending_division_title,
        'popular_categories':popular_categories

    }
    return render(request,'home/home.html', context)

def display_categories_post(request,id):
    categories = Categories.objects.get(id=id)
    products = Product.objects.filter(categories=categories)
    context = {
        'products':products
    }
    return render(request,'categories-post.html',context)