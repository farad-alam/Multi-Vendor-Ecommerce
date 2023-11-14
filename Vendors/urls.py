from django.urls import path
from .import views
urlpatterns = [
    path('vendor/registration/', views.vendor_registration, name='vendor_registration'),
    path('vendor/vendor-store/<int:store_id>',views.vendor_store_with_product, name='vendor_store_with_product')
]