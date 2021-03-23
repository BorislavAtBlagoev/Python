from django.db import models
from users.models import User
from categories.models import Category


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    code = models.PositiveSmallIntegerField(unique=True, null=False)
    description = models.CharField(max_length=300, blank=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='product_category')
    price = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_updated_by')

    def __str__(self):
        return self.name
