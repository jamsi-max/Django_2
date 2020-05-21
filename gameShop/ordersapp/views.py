from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.db import transaction
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.http import JsonResponse
from django.template.loader import render_to_string

from ordersapp.models import Order, OrderItem
from basketapp.models import Basket
from mainapp.models import Product
from ordersapp.forms import OrderForm, OrderItemForm


def order_forming_complete(request, pk):
   order = get_object_or_404(Order, pk=pk)
   order.status = Order.SENT_TO_PROCEED
   order.save()

   return HttpResponseRedirect(reverse('ordersapp:index'))


class OrderList(ListView):
    model = Order

    def get_queryset(self):
       return self.model.objects.filter(user=self.request.user, is_active=True)


class OrderItemsCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        formset = None
        if self.request.method == 'POST':
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        elif self.request.method == 'GET':
            basket_items = self.request.user.basket.all()
            if basket_items.count():
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    basket_item = basket_items[num]
                    form.initial['product'] = basket_item.product
                    form.initial['quantity'] = basket_item.quantity
                    form.initial['price'] = basket_item.product.price
                # basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):

        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            self.request.user.basket.all().delete()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderItemsUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('ordersapp:index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.method == 'POST':
            data['orderitems'] = OrderFormSet(self.request.POST, self.request.FILES, instance=self.object)
        elif self.request.method == 'GET':
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = round(form.instance.product.get_discount_price, 2)
            data['orderitems'] = formset
 

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()


        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:index')


class OrderRead(DetailView):
    model = Order
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'order/view'
        return context


@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
   instance.product.quantity += instance.quantity
   instance.product.save()


class OrderPriceView(View):
    def get(self, request):
        obj = get_object_or_404(Product, pk=request.GET['data'])
        return JsonResponse({'result': round(obj.get_discount_price, 2)}, status=200)

        