from django import forms

from ordersapp.models import Order, OrderItem
from adminapp.utils import FormWidgetMixin

class OrderForm(FormWidgetMixin, forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'is_active', 'status')

    class_all_fields = 'form-control'


class OrderItemForm(FormWidgetMixin, forms.ModelForm):
    price = forms.CharField(label='price', min_length=1, max_length=16, required=False)
    class Meta:
        model = OrderItem
        fields = '__all__'

    class_all_fields = 'form-control'