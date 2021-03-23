from django.contrib.auth.models import AbstractUser
from django.db import models

from users.choices import roles


class User(AbstractUser):
    password = None
    first_name = None
    last_name = None
    email = None
    user_role_type = models.PositiveSmallIntegerField(choices=roles, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Admin(models.Model):
    is_registered_admin = models.BooleanField(default=False)
