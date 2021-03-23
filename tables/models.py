from django.db import models

from users.models import User


class Table(models.Model):
    number = models.PositiveSmallIntegerField(unique=True, null=False)
    capacity = models.PositiveSmallIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='table_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='table_updated_by')

    def __str__(self):
        return str(self.id)
