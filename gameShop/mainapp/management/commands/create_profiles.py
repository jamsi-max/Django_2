from django.core.management.base import BaseCommand

from authapp.models import ShopUser, ShopUserProfile

class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in ShopUser.objects.all():
            shopuserprofile = ShopUserProfile(user=user)
            shopuserprofile.save()

