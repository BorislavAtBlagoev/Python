"""restaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from categories.views import CategoryViewSet
from images.views import ImageViewSet
from orders.views import OrderViewSet, OrdersProductsViewSet, get_active_orders_by_table_id, soft_delete
from products.views import ProductViewSet
from tables.views import TableViewSet, list_tables
from users.views import sign_up_user

router = routers.SimpleRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'tables', TableViewSet)
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'orders_products', OrdersProductsViewSet)
router.register(r'images', ImageViewSet, basename='images')

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('__debug__/', include(debug_toolbar.urls)),
                  path('api-auth/', include('rest_framework.urls')),
                  path('table/<int:pk>/', get_active_orders_by_table_id),
                  path('sign_up/', sign_up_user),
                  path('soft_delete/<int:pk>/', soft_delete),
                  path('list_tables/', list_tables)
              ] + router.urls
