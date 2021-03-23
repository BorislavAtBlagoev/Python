from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    description = models.CharField(max_length=300, blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_updated_by')

    def __str__(self):
        return self.name
