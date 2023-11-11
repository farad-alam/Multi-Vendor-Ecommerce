from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from . models import CustomUser

class RegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email','first_name', 'last_name','mobile', 'password1', 'password2')  # Add any other fields you want to include in the registration form


