from django.urls import path, re_path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    re_path(r'^$', mainapp.products, name='index'),
    re_path(r'^category/(?P<pk>\d+)/(?P<page>\d+)/$', mainapp.products, name='category'),
    re_path(r'^(?P<pk>\d+)/$', mainapp.product, name='product'),
]