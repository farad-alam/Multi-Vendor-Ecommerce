from django.contrib import admin
from products.admin import super_admin_site

from . models import SliderArea, DisplayHotProductInCategories, PopularCategories
# Register your models here.
super_admin_site.register(SliderArea)
super_admin_site.register(DisplayHotProductInCategories)
super_admin_site.register(PopularCategories)

