from django.shortcuts import render, get_object_or_404, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View, DetailView
from django.urls import reverse_lazy

from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection


from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product, News
from ordersapp.models import Order, OrderItem
from adminapp.forms import AdminNewsAddForm, AdminCreateUserForm, AdminUpdateUserForm, AdminCreateCategoryForm, AdminCreateProductForm
from adminapp.forms import AdminCreateOrderForm, AdminUpdateProductForm
from adminapp.utils import SuperuserCheckMixin, SoftDeleteMixin, TitleMixin

from ordersapp.views import OrderItemsCreate, OrderItemsUpdate, OrderRead

class UserListView(SuperuserCheckMixin, TitleMixin, ListView):
    title = 'Admin: User'
    model = ShopUser


class UserOrdersView(SuperuserCheckMixin, TitleMixin, ListView):
    title = 'Admin: User Orders'
    model = Order
    template_name = 'adminapp/user_orders.html'

    def get_queryset(self):
       return self.model.objects.filter(user__pk = self.kwargs['pk'], is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = ShopUser.objects.filter(pk=self.kwargs['pk'])[0]
        return context

class UserCreateView(SuperuserCheckMixin, TitleMixin, CreateView):
    title = 'Admin: Create User'
    model = ShopUser
    success_url = reverse_lazy('admin:index')
    form_class = AdminCreateUserForm


class UserUpdateView(SuperuserCheckMixin, TitleMixin, UpdateView):
    title = 'Admin: Update User'
    model = ShopUser
    success_url = reverse_lazy('admin:index')
    form_class = AdminUpdateUserForm


class UserDeleteView(SuperuserCheckMixin, TitleMixin, SoftDeleteMixin, DeleteView):
    title = 'Admin: Delete User'
    model = ShopUser
    success_url = reverse_lazy('admin:index')


class CategoryListView(SuperuserCheckMixin, TitleMixin, ListView):
    title = 'Admin: Category'
    model = ProductCategory


class CategoryCreateView(SuperuserCheckMixin, TitleMixin, CreateView):
    title = 'Admin: Create Category'
    model = ProductCategory
    success_url = reverse_lazy('admin:category')
    form_class = AdminCreateCategoryForm


class CategoryUpdateView(SuperuserCheckMixin, TitleMixin, UpdateView):
    title = 'Admin: Update Category'
    model = ProductCategory
    success_url = reverse_lazy('admin:category')
    form_class = AdminCreateCategoryForm


class CategoryDeleteView(SuperuserCheckMixin, TitleMixin, SoftDeleteMixin, DeleteView):
    title = 'Admin: Delete Category'
    model = ProductCategory
    success_url = reverse_lazy('admin:category')

# class ProductListView(SuperuserCheckMixin, TitleMixin, ListView):
#     title = 'Admin: Category'
#     model = Product

@user_passes_test(lambda x: x.is_superuser)
def product(request, pk, page=1):
    category = get_object_or_404(ProductCategory, pk=int(pk))
    product_list = category.product_set.all().order_by('-is_active', 'name')

    paginator = Paginator(product_list, 5)
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)

    content = {
        'page_title': 'admin: products',
        'category': category,
        'object_list': product_list,
        'mediaURL': settings.MEDIA_URL,
    }
    return render(request, 'mainapp/product_list.html', context=content)


class ProductCreateView(SuperuserCheckMixin, TitleMixin, CreateView):
    title = 'Admin: Create Product'
    model = Product
    success_url = reverse_lazy('admin:category')
    form_class = AdminCreateProductForm


class ProductUpdateView(SuperuserCheckMixin, TitleMixin, UpdateView):
    title = 'Admin: Update Product'
    model = Product
    success_url = reverse_lazy('admin:category')
    form_class = AdminCreateProductForm


class ProductDeleteView(SuperuserCheckMixin, TitleMixin, SoftDeleteMixin, DeleteView):
    title = 'Admin: Delete Product'
    model = Product
    success_url = reverse_lazy('admin:category')


class NewsListView(SuperuserCheckMixin, TitleMixin, ListView):
    title = 'Admin: News'
    model = News


class NewsCreateView(SuperuserCheckMixin, TitleMixin, CreateView):
    title = 'Admin: Create News'
    model = News
    success_url = reverse_lazy('admin:news')
    form_class = AdminNewsAddForm


class NewsUpdateView(SuperuserCheckMixin, TitleMixin, UpdateView):
    title = 'Admin: Update News'
    model = News
    success_url = reverse_lazy('admin:news')
    form_class = AdminNewsAddForm


class NewsDeleteView(SuperuserCheckMixin, TitleMixin, SoftDeleteMixin, DeleteView):
    title = 'Admin: Delete News'
    model = News
    success_url = reverse_lazy('admin:news')


class OrdersListView(SuperuserCheckMixin, TitleMixin, ListView):
    title = 'Admin: Orders'
    model = Order
    template_name = 'adminapp/order_list.html'


class OrdersUpdateView(SuperuserCheckMixin, TitleMixin, OrderItemsUpdate):
    title = 'Admin: Update Orders'
    model = Order
    success_url = reverse_lazy('admin:orders')
    form_class = AdminUpdateProductForm
    template_name = 'adminapp/order_form.html'


class OrdersDeleteView(SuperuserCheckMixin, TitleMixin, DeleteView):
    title = 'Admin: Delete Orders'
    model = Order
    template_name = 'adminapp/order_confirm_delete.html'
    success_url = reverse_lazy('admin:orders')


class OrdersRead(SuperuserCheckMixin, TitleMixin, OrderRead):
    title = 'Admin: Orders Detail'
    success_url = reverse_lazy('admin:orders')
    template_name = 'adminapp/order_detail.html'


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]

@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)