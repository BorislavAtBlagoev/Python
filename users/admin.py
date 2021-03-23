from django.contrib import admin
from categories.models import Category
from orders.models import Order, Table
from products.models import Product

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Table)
admin.site.register(Product)
#admin.site.register(OrdersProducts)
