from django.contrib import admin
from products.models import *
from . placed_oder_and_items_admin import OderManagementAdmin 
from . complete_oder_and_items_admin import CompleteOderModelAdmin
# Register your models here.

class CustomOderManagementAdminSite(admin.AdminSite):
    site_header = 'Oder Management'
    site_title = 'Oder Management Dashboard'
    index_title = 'Welcome to Oder Management'

    def has_permission(self, request):
        # Check if the user is authenticated and has the role "Editor" (user_role == 2)
        return request.user.is_authenticated and request.user.user_role == '2'
    
    login_view = 'custom_admin:login'  # The URL name for your custom login view
custom_oderManagement_admin_site = CustomOderManagementAdminSite(name='customodermanagement')

custom_oderManagement_admin_site.register(PlacedOder,OderManagementAdmin)
custom_oderManagement_admin_site.register(CompletedOder,CompleteOderModelAdmin)
custom_oderManagement_admin_site.register(Product)

