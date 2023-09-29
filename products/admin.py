from django.contrib import admin
from . models import *
# Register your models here.

class ProductImages(admin.TabularInline):
    model = ProductImage

class ProductAditionalInformations(admin.TabularInline):
    model = ProductAditionalInformation


class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImages,ProductAditionalInformations)
    list_display = ['title','categories','regular_price']

class CartModelAdmin(admin.ModelAdmin):
    list_display = ['product','user']

admin.site.register(Industry)
admin.site.register(Categories)
admin.site.register(SubCategories)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductAditionalInformation)
admin.site.register(Cart,CartModelAdmin)
admin.site.register(CustomerAddress)
admin.site.register(PlacedOder)
admin.site.register(PlacedeOderItem)
admin.site.register(CuponCodeGenaration)

