from django.urls import path
from . import views
urlpatterns = [
    path('product-details/<slug:slug>', views.product_details, name='product_details'),
    path('add-to-cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('show-cart/', views.show_cart, name='show_cart'),
    path('increse-cart/', views.increase_cart, name='increase_cart'),
    path('checkout/', views.check_out, name='check_out'),
    path('placed-oder/', views.placed_oder, name='placed_oder'),
    path('cupon-apply/', views.cupon_apply, name='cupon_apply'),
    path('add-product-review/', views.add_product_review_and_rating, name='add_product_review_and_rating'),
    path('save-shipping-address/', views.save_shipping_address, name='save_shipping_address'),
    
]