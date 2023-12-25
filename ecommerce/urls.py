"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from AdminPanel.admin import employee_Management_admin_site
from Vendors.admin import vendor_admin_site
from products.admin import super_admin_site
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('super-admin/', super_admin_site.urls),
    path('employee-dashboard/', employee_Management_admin_site.urls),
    path('vendor-dashboard/', vendor_admin_site.urls),
    path('', include("accounts.urls") ),
    path('', include('products.urls')),
    path('', include('home.urls')),
    path('', include('AdminPanel.urls')),
    path('', include('Vendors.urls')),
    path('', include('payments.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
