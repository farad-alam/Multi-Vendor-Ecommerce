from django.urls import path
from .import views
urlpatterns = [
    path('admin-panel/dashboard/', views.dashboard, name='dashboard'),
    path('admin-panel/placed-oder-list/', views.show_placed_oder_list, name='show_placed_oder_list'),
    path('admin-panel/completed-oder-list/', views.show_completed_oder_list, name='show_completed_oder_list'),
    path('admin-panel/placed-oder-item-list/<int:id>', views.show_placed_oder_item_list, name='show_placed_oder_item_list'),
    path('admin-panel/completed-oder-item-list/<int:id>', views.show_completed_oder_item_list, name='show_completed_oder_item_list'),
]
