from django.db import models

from django.conf import settings
from mainapp.models import Product

class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    created_at = models.DateTimeField(verbose_name='время', auto_now_add=True)

    def __str__(self):
        return self.user
    
    @property
    def get_price(self):
        return self.get_discount_price * self.quantity if self.product.discount else self.product.price * self.quantity

    @property
    def get_discount_price(self):
        return float(self.product.price) - (float(self.product.price) * (self.product.discount / 100))

    @property
    def get_quantity(self):
        return sum([item.quantity for item in self.user.basket.all()]) 

    @property
    def get_total(self):
        total_price = []
        for item in self.user.basket.all():
            if item.product.discount:
                total_price.append(item.get_discount_price*item.quantity)
            else:
                total_price.append(float(item.get_price))
        return sum(total_price)


    