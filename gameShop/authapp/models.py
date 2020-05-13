from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

from adminapp.utils import togle_active


def det_expires_datetime():
    return now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name="age", default=18)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=det_expires_datetime)

    def is_activation_key_expired(self):
        return now() > self.activation_key_expires

    def soft_delete(self):
        togle_active(self)

    class Meta:
        ordering = ['-is_active', '-is_superuser', 'username']


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'M'),
        (FEMALE, 'W'),
    )

    user = models.OneToOneField(ShopUser, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, \
                               blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512, \
                               blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, \
                              choices=GENDER_CHOICES, blank=True) 
    
    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)
        else:
            instance.shopuserprofile.save()

            

