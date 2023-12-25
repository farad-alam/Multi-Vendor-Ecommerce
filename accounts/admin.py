from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from accounts.forms import RegistrationForm
from products.admin import super_admin_site


class CustomUserAdmin(UserAdmin):

    class Meta(UserChangeForm.Meta):
        model = CustomUser

    form = RegistrationForm
    list_display = ('email', 'id', 'first_name', 'last_name', 'mobile','user_role','is_active', 'is_staff', 'is_superuser')

    fieldsets = (
        # (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ( 'user_role','is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'mobile')}),
        ('Permissions', {'fields': ('user_role','is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    ordering = ('email',)
    search_fields = ("first_name", "last_name", "email")

super_admin_site.register(CustomUser, CustomUserAdmin)



