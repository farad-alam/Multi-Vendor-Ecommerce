from django.contrib import admin
from products.models import *
from . placed_oder_and_items_admin import OderManagementAdmin 
from . complete_oder_and_items_admin import CompleteOderModelAdmin
# Register your models here.

class CustomOderManagementAdminSite(admin.AdminSite):
    site_header = 'Employee Dahboard'
    site_title = 'Manage Oders - Customers - Sellers'
    index_title = 'Manage Oders - Customers - Sellers'

    def has_permission(self, request):
        # Check if the user is authenticated and has the role "Editor" (user_role == 2)
        return request.user.is_authenticated and request.user.user_role == '2'
    
    login_view = 'employee_admin:login'  # The URL name for your custom login view
employee_Management_admin_site = CustomOderManagementAdminSite(name='employee_admin_site')

employee_Management_admin_site.register(PlacedOder,OderManagementAdmin)
employee_Management_admin_site.register(CompletedOder,CompleteOderModelAdmin)
employee_Management_admin_site.register(Product)

