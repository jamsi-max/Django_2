from django.db import models

from django.conf import settings
from mainapp.models import Product
from adminapp.utils import togle_active


class Order(models.Model):
    FORMING = 'F'
    SENT_TO_PROCEED = 'S'
    PROCEEDED = 'P'
    PAID = 'D'
    READY = 'R'
    CANCEL = 'C'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'forming'),
        (SENT_TO_PROCEED, 'sent to proceed'),
        (PAID, 'paid'),
        (PROCEEDED, 'proceeded'),
        (READY, 'ready'),
        (CANCEL, 'cancel'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='created', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated', auto_now=True)
    status = models.CharField(verbose_name='status', 
                              max_length=1,
                              choices=ORDER_STATUS_CHOICES, 
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='active', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'Current order: {self.id}'

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(map(lambda x: x.quantity * (float(x.product.price) - float((x.product.price * x.product.discount / 100))), items)),
            'total_quantity': sum(map(lambda x: x.quantity, items))
        }

    def get_total_quantity(self):
        return sum(map(lambda x: x.quantity, self.orderitems.select_related()))

    def get_product_type_quantity(self):
        return self.orderitems.count()

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(map(lambda x: x.quantity * (float(x.product.price) - float((x.product.price * x.product.discount / 100))), items))

    def delete(self,  *args, **kwargs):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        # self.is_active = False
        togle_active(self)
        self.save()



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity', default=0)

    @property
    def get_product_cost(self):
        return  self.quantity * (float(self.product.price) - (float(self.product.price) * self.product.discount/100))

    @classmethod
    def get_item(cls, pk):
        try:
            return cls.objects.get(pk=pk)
        except Exception as e:
            print(e)

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super().save(*args, **kwargs)
