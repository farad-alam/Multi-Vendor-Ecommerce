from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.registration_view, name='registration_view'),
    path('login/', views.login_view, name='user_login'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('user-logout/', views.user_logout, name='user_logout'),
]
