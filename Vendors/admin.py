from typing import Any
from django.contrib import admin
from django.urls.resolvers import URLPattern
from .models import VendorStore
from products.models import Product, ProductImage, ProductAditionalInformation
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.html import format_html
# Register your models here.

class CustomVendorAdminSite(admin.AdminSite):
    site_header = 'MVEC Seller Dashboard'
    site_title = 'Seller Dashboard'
    index_title = 'Track Your Performence'

    def has_permission(self, request):
        # Check if the user is authenticated and has the role "Vendor" (user_role == 3)
        return request.user.is_authenticated and request.user.user_role == '3'
    
vendor_admin_site = CustomVendorAdminSite(name='custom_vendor_admin_site')

class VebdorStoreModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'user','created_at')
    
    # For creting New Instance -> Using these sields
    fieldsets = (
        (
            (None,{'fields':('name', 'slug','logo', 'cover_photo')})
        ),
    )

    def save_model(self, request, obj, form, change):
        if VendorStore.objects.filter(user=request.user).__len__ () < 3:
            obj.user = request.user
            obj.save()
            return super().save_model(request, obj, form, change)
        else:
            messages.info(request, f"{request.user} cant create more than 3 Store")
            return redirect('/vendor-dashboard/Vendors/vendorstore/')


class ProductImageTabular(admin.TabularInline):
    model = ProductImage
    extra = 0

class ProductAditonalInformationTabular(admin.TabularInline):
    model = ProductAditionalInformation
    extra = 0
    
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('title','formated_stoc','discounted_price','categories','sort_descriptions')
    inlines = (ProductImageTabular,ProductAditonalInformationTabular)

    @admin.display(description='Description')
    def sort_descriptions(self,obj):
        return obj.description.replace('<p>','')[:30]

    @admin.display(description='Stock Product')
    def formated_stoc(self,obj):
        return format_html('<strong style="color:#008000;">{}</strong>',obj.stoc)
    

vendor_admin_site.register(VendorStore, VebdorStoreModelAdmin)
vendor_admin_site.register(Product, ProductModelAdmin)