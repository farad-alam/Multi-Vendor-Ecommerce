from django.urls import path
from . import views


urlpatterns = [
    path('payment-details/',views.display_payment_details, name='display_payment_details'),
    path('create-payment-intent/', views.create_checkout_session, name='strip_checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    
]
