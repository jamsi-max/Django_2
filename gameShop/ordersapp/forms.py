from django import forms

from ordersapp.models import Order, OrderItem
from adminapp.utils import FormWidgetMixin

class OrderForm(FormWidgetMixin, forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'is_active', 'status')

    class_all_fields = 'form-control'


class OrderItemForm(FormWidgetMixin, forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()

    class_all_fields = 'form-control'