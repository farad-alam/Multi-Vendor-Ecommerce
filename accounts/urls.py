from django.urls import path
from . import views
urlpatterns = [
    path('user/register/', views.registration_view, name='registration_view'),
    path('user/login/', views.login_view, name='user_login'),
    path('user/dasboard/', views.user_dashboard, name='user_dashboard'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path('user/logout/', views.user_logout, name='user_logout'),
]
