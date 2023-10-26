from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from . models import CustomUser

class RegistrationForm(UserCreationForm):
    # password1 = forms.CharField(
    #     label="Password",
    #     widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    # )
    # password2 = forms.CharField(
    #     label="Password confirmation",
    #     widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    # )

    class Meta:
        model = CustomUser
        fields = ('email','first_name', 'last_name','mobile', 'password1', 'password2')  # Add any other fields you want to include in the registration form
        # fields = '__all__'
    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords do not match.")
    #     return password2

