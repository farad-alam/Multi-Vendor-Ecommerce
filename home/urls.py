from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('categoris/<int:id>', views.display_categories_post, name='display_categories_post'),
    path('test-page/', views.test_page,),


]