from django.urls import path, re_path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    re_path(r'^$', adminapp.UserListView.as_view(), name='index'),
    re_path(r'^user/orders/(?P<pk>\d+)/$', adminapp.UserOrdersView.as_view(), name='user_orders'),
    re_path(r'^user/create/$', adminapp.UserCreateView.as_view(), name='user_create'),
    re_path(r'^user/update/(?P<pk>\d+)/$', adminapp.UserUpdateView.as_view(), name='user_update'),
    re_path(r'^user/delete/(?P<pk>\d+)/$', adminapp.UserDeleteView.as_view(), name='user_delete'),

    re_path(r'^category/$', adminapp.CategoryListView.as_view(), name='category'),
    re_path(r'^category/create/$', adminapp.CategoryCreateView.as_view(), name='category_create'),
    re_path(r'^category/update/(?P<pk>\d+)/$', adminapp.CategoryUpdateView.as_view(), name='category_update'),
    re_path(r'^category/delete/(?P<pk>\d+)/$', adminapp.CategoryDeleteView.as_view(), name='category_delete'),

    re_path(r'^product/(?P<pk>\d+)/(?P<page>\d+)/$', adminapp.product, name='product'),
    # re_path(r'^product/(?P<pk>\d+)/(?P<page>\d+)/$', adminapp.ProductListView.as_view(), name='product'),
    re_path(r'^product/create/$', adminapp.ProductCreateView.as_view(), name='product_create'),
    re_path(r'^product/update/(?P<pk>\d+)/$', adminapp.ProductUpdateView.as_view(), name='product_update'),
    re_path(r'^product/delete/(?P<pk>\d+)/$', adminapp.ProductDeleteView.as_view(), name='product_delete'),
    
    re_path(r'^news/$', adminapp.NewsListView.as_view(), name='news'),
    re_path(r'^news/add/$', adminapp.NewsCreateView.as_view(), name='news_add'),
    re_path(r'^news/update/(?P<pk>\d+)/$', adminapp.NewsUpdateView.as_view(), name='news_update'),
    re_path(r'^news/delete/(?P<pk>\d+)/$', adminapp.NewsDeleteView.as_view(), name='news_delete'),

    re_path(r'^order/$', adminapp.OrdersListView.as_view(), name='orders'),
    re_path(r'^order/read/(?P<pk>\d+)/$', adminapp.OrdersRead.as_view(), name='order_read'),
    # re_path(r'^order/create/$', adminapp.OrdersCreateView.as_view(), name='order_create'),
    re_path(r'^order/update/(?P<pk>\d+)/$', adminapp.OrdersUpdateView.as_view(), name='order_update'),
    re_path(r'^order/delete/(?P<pk>\d+)/$', adminapp.OrdersDeleteView.as_view(), name='order_delete'),
]