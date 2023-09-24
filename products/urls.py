from django.urls import path
from . import views
urlpatterns = [
    path('product/<slug:slug>', views.product_details, name='product_details'),
    path('add-to-cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('show-cart/', views.show_cart, name='show_cart'),
    path('increse-cart/', views.increase_cart, name='increase_cart'),
    
]