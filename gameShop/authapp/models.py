from django.db import models
from django.contrib.auth.models import AbstractUser

from adminapp.utils import togle_active


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name="age")

    def soft_delete(self):
        togle_active(self)

    class Meta:
        ordering = ['-is_active', '-is_superuser', 'username'] 

