# from django.contrib import admin
# from . models import CustomUser
# # Register your models here.


# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('email', 'first_name', 'last_name', 'mobile')
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal Info', {'fields': ('first_name', 'last_name', 'mobile')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2'),
#         }),
#     )

# admin.site.register(CustomUser, CustomUserAdmin)


from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from accounts.forms import RegistrationForm

class CustomUserAdmin(UserAdmin):

    class Meta(UserChangeForm.Meta):
        model = CustomUser

    form = RegistrationForm
    list_display = ('email', 'first_name', 'last_name', 'mobile','user_role','is_active', 'is_staff', 'is_superuser')

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

    # def save_model(self, request, obj, form, change):
    #     obj.save()
    #     if change:  # Check if it's an update
    #         # Capture the original email and password
    #         original_email = obj.email
    #         original_password = obj.password  # Ensure you have a mechanism to capture the original password securely
    #         print(original_password)
    #         # Call the parent class's save_model to handle the rest of the save process
    #         super().save_model(request, obj, form, change)

    #         # Set the email and password back to their original values
    #         obj.email = original_email
    #         obj.password = original_password  # You may need to use a secure method to reset the password

    #         # Save the object again to ensure that the email and password remain unchanged
    #         obj.save()

admin.site.register(CustomUser, CustomUserAdmin)


# class CustomUserAdminForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'mobile', 'is_active', 'is_staff', 'is_superuser','email',)

# class CustomUserChangeForm(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = CustomUser
#         fields = ('first_name', 'last_name', 'mobile', 'is_active', 'is_staff', 'is_superuser','email',)
#         field_classes = {"username": 'email'}


# class CustomUserAdmin(UserAdmin):
#     form = CustomUserChangeForm
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2'),
#         }),
#         ('details',{
#             'classes':('wide',),
#             'fields': ('first_name', 'last_name', 'mobile', 'is_active', 'is_staff', 'is_superuser')
#         }),
#     )
#     ordering = ('email',)
#     search_fields = ("first_name", "last_name", "email")
#     list_display = ('email', 'first_name', 'last_name', 'mobile', 'is_active', 'is_staff', 'is_superuser')



