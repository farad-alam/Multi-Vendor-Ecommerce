from django.contrib import admin
from . models import *
from django.contrib.auth.models import Group

# Register your models here.


class SuperAdminSite(admin.AdminSite):
    site_header = 'Super Admin Dashboard'
    site_title = 'Super Admin Dashboard'
    index_title = 'Control Your Site From Here'

    def has_permission(self, request):
        # Check if the user is authenticated and has the role "Admin" (user_role == 1)
        return request.user.is_authenticated and request.user.is_superuser

    login_view = 'superadmin:login'  # The URL name for the default admin login view

super_admin_site = SuperAdminSite(name='superadminsite')



class ProductImages(admin.TabularInline):
    model = ProductImage

class ProductAditionalInformations(admin.TabularInline):
    model = ProductAditionalInformation


class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImages,ProductAditionalInformations)
    list_display = ['title','categories','regular_price','vendor_stores']
    list_editable =['vendor_stores']

class CartModelAdmin(admin.ModelAdmin):
    list_display = ['product','user']

super_admin_site.register(Industry)
super_admin_site.register(Categories)
super_admin_site.register(SubCategories)
super_admin_site.register(Product,ProductAdmin)
super_admin_site.register(ProductImage)
super_admin_site.register(ProductAditionalInformation)
super_admin_site.register(Cart,CartModelAdmin)
super_admin_site.register(CustomerAddress)
super_admin_site.register(PlacedOder)
super_admin_site.register(PlacedeOderItem)
super_admin_site.register(CuponCodeGenaration)
super_admin_site.register(CompletedOder)
super_admin_site.register(CompletedOderItems)
super_admin_site.register(ProductStarRatingAndReview)
super_admin_site.register(Group)





