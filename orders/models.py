from django.db import models

from tables.models import Table
from users.models import User
from products.models import Product
from orders.choices import status


class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='table')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service')
    status = models.CharField(max_length=20, choices=status, null=False, default='In progress')
    products = models.ManyToManyField(Product, through='OrdersProducts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_updated_by')
    is_deleted = models.BooleanField(null=False, default=0)

    def __str__(self):
        return str(self.id)


class OrdersProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(null=False, default=1)

    @property
    def get_price(self):
        return self.product.price

    class Meta:
        unique_together = ('order', 'product',)
