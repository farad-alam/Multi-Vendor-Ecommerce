from django.urls import path
from .import views
urlpatterns = [
    path('vendor/registration/', views.vendor_registration, name='vendor_registration')
]