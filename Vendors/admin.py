from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(user=request.user)
        return queryset

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
    
    list_display = ('title','formated_stoc','discounted_price','categories', 'vendor_stores', 'sort_descriptions')
    list_editable = ('categories','vendor_stores')
    readonly_fields = ['slug']

    fieldsets = [
        (
            'Product Identety', {
                'fields':['title','slug','vendor_stores']
            }
        ),
        (
            'Prices & Stoc', {
            'classes': ('collapse',),
            'fields':[('regular_price','discounted_parcent','stoc','out_of_stoc')]
            }
        ),
        (
            'Descriptions',{
                'classes': ('collapse',),
                'fields':[('modle','tag','categories'),'description']
            }
        ),
        (
            'Details Description',{
                'fields':['details_description']
            }
        ),
        
    ]
    
    inlines = (ProductImageTabular,ProductAditonalInformationTabular)


    def get_queryset(self, request):
        # Override the queryset to filter products by the current user's vendor
        qs = super().get_queryset(request)
        
        vendore_store_name = 'admin-store'
        try:
            # get the targeted vendor store instance
            vendor_store = VendorStore.objects.get(name=vendore_store_name)
        except VendorStore.DoesNotExist:
            return qs.none()
        
        # Filter products by the specified VendorStore
        qs = qs.filter(vendor_stores=vendor_store)
        return qs
    
    @admin.display(description='Description')
    def sort_descriptions(self,obj):
        return obj.description.replace('<p>','').replace('</p>','')[:30]

    @admin.display(description='Stock Product')
    def formated_stoc(self,obj):
        return format_html('<strong style="color:#008000;">{}</strong>',obj.stoc)
    
    formated_stoc.short_description = "Available in Stock"

    def save_model(self, request, obj, form, change):
        if request.user.user_role == '3':
            obj.save()

        return super().save_model(request, obj, form, change)
    

vendor_admin_site.register(VendorStore, VebdorStoreModelAdmin)
vendor_admin_site.register(Product, ProductModelAdmin)

admin.site.register(VendorStore)