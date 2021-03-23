from django.db import models

from users.models import User


class Image(models.Model):
    image = models.ImageField(upload_to='images/', max_length=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.image
