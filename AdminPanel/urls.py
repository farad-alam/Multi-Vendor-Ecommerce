from django.urls import path
from .import views
urlpatterns = [
    path('admin-panel/placed-oder-list/', views.show_placed_oder_list, name='show_placed_oder_list'),
    path('admin-panel/placed-oder-item-list/<int:id>', views.show_placed_oder_item_list, name='show_placed_oder_item_list'),
]
