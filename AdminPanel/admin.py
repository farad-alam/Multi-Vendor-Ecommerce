from django.contrib import admin
from django.forms import inlineformset_factory
from products.models import *
from accounts.models import *
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied


# Register your models here.

class PlacedOderItemAdmin(admin.TabularInline):
    model = PlacedeOderItem
    extra = 0
    
class OderManagementAdmin(admin.ModelAdmin):
    list_display = ['order_number','sub_total_price','paid','user']
    list_editable = ['paid']
    list_filter = ['status','placed_date']
    inlines = (PlacedOderItemAdmin,)

    def has_change_permission(self, request, obj=None):
        # Grant change permission to staff users
        return request.user.is_staff
    


    def save_model(self, request, obj, form, change):
        # Check if the user has permission to create PlacedeOderItem

        # request.user.user_permissions.add(
        # Permission.objects.get(codename='add_placedoder'),
        # Permission.objects.get(codename='change_placedoder'),
        # Permission.objects.get(codename='delete_placedoder'),        
        # Permission.objects.get(codename='add_placedeoderitem'),        
        # Permission.objects.get(codename='change_placedeoderitem'),        
        # Permission.objects.get(codename='delete_placedeoderitem'),        
        # Permission.objects.get(codename='add_customeraddress'),        
        # Permission.objects.get(codename='change_customeraddress'),        
        # Permission.objects.get(codename='delete_customeraddress'),        
        # Permission.objects.get(codename='add_customuser'),        
        # Permission.objects.get(codename='change_customuser'),        
        # Permission.objects.get(codename='delete_customuser'),        
        # )
        def get_model_perms(self, request):
            return {
                "add": self.has_add_permission(request),
                "change": self.has_change_permission(request),
                "delete": self.has_delete_permission(request),
                "view": self.has_view_permission(request),
            }
        if not request.user.has_perm('placedoder.add_placedeoderitem'):
            # Handle permission denied, e.g., raise an exception or redirect
            raise PermissionDenied("You do not have permission to create PlacedeOderItem.")
    
        obj.save()
        print(obj.pk)
        super().save_model(request, obj, form, change)

        if change == False:
            # Create and associate 'PlacedOderItem' instances without saving them immediately
            PlacedeOderItemFormSet = inlineformset_factory(PlacedOder, PlacedeOderItem, fields=('product', 'quantity'))
            formset = PlacedeOderItemFormSet(request.POST, instance=obj)
            
            if formset.is_valid():
                formset.save()
        
class CustomOderManagementAdminSite(admin.AdminSite):
    site_header = 'Oder Management'
    site_title = 'Oder Management Dashboard'
    index_title = 'Welcome to Oder Management'

custom_oderManagement_admin_site = CustomOderManagementAdminSite(name='customodermanagement')

custom_oderManagement_admin_site.register(PlacedOder,OderManagementAdmin)
custom_oderManagement_admin_site.register(Product)
