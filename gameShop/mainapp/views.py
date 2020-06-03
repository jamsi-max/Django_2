from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.cache import cache
from django.views.decorators.cache import cache_page

import random, os

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product, MainSocial, Services, News, Team
from django.conf import settings

from authapp.forms import ShopUserLoginForm

# function upload data from file json
# !!! ONLY UTF-8 decode
# import json
# import os
# def get_data():
#     try:
#         with open(os.path.abspath('data.json'), 'r', encoding="utf-8") as file:
#             data = json.load(file)
#     except:
#         print("Error load data from BD")
#         data = []
#     return data

# CACHE REDIS
def get_links_menu():
    return ProductCategory.objects.filter(is_active=True)
    # if settings.LOW_CACHE:
    #     key = 'links_menu'
    #     links_menu = cache.get(key)
    #     print('*'*50)
    #     print(ProductCategory.objects.all())
    #     print(links_menu)
    #     if links_menu is None:
    #         links_menu = ProductCategory.objects.filter(is_active=True)
    #         cache.set(key, links_menu)
    #     return links_menu
    # else:
    #     return ProductCategory.objects.filter(is_active=True)

def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')              
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')

def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)

def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('name')                  
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('name')
                              
                                 

def get_same_products(current_product):
    same_products = list(current_product.category.product_set.filter(is_active=True).exclude(pk=current_product.pk))
    return random.sample(same_products, 4) if len(same_products) > 4 else same_products
  
def get_name(current_product):
    return current_product.name.split(':')

def get_discount_list():
    return [_ for _ in Product.objects.filter(is_active=True).exclude(discount=0)]


def index(request):
    services = Services.objects.all()
    products_list = get_products() #Product.objects.filter(is_active=True)
    main_social = MainSocial.objects.all()
    news = News.objects.filter(is_active=True).order_by('-data')[:3]
    team = Team.objects.all()[:4]
    content = {
        'page_title': 'main',
        'social_links': main_social,
        'products_list': random.sample(list(products_list), 4),
        'services': services,
        'news': news,
        'team': team,
        'mediaURL': settings.MEDIA_URL,
        'login_form': ShopUserLoginForm(),
    }
    return render(request, 'mainapp/index.html', context=content)


def products(request, pk=None, page=1):
    #!!!!!!!!!!! Create two product discount 
    # it = random.sample(get_discount_list(),2)

    if int(pk) is not None and int(pk) != 0:
        products_list = get_products_in_category_orederd_by_price(pk) #Product.objects.filter(category__pk=pk, is_active=True).order_by('name')
    else:
        products_list = get_products().order_by('name') #Product.objects.filter(is_active=True).order_by('name')
        
    category = get_links_menu()

    paginator = Paginator(products_list, 8)
    try:
        products_list = paginator.page(page)
    except PageNotAnInteger:
        products_list = paginator.page(1)
    except EmptyPage:
        products_list = paginator.page(paginator.num_pages)

    content = {
        'pk': pk,
        'page_title': 'gallery',
        'products_list': products_list,
        'category': category,
        'mediaURL': settings.MEDIA_URL,
        'login_form': ShopUserLoginForm(),
    }
    if request.is_ajax():
        result = render_to_string('includes/inc__product_item.html', context=content)
        result_paginator = render_to_string('includes/inc__paginator.html', context={'pk': pk, 'products_list': products_list})
        return JsonResponse({'result': result, 'paginator': result_paginator})
        
    return render(request, 'mainapp/products.html', context=content)


def product(request, pk):
    current_product = get_product(pk) #get_object_or_404(Product, pk=pk)
    content = {
        'page_title': 'product',
        'current_name_list': get_name(current_product),
        'page_title': 'product',
        'current_product': current_product,
        'products_list': get_same_products(current_product)[:4],
        'login_form': ShopUserLoginForm(),
        'mediaURL': settings.MEDIA_URL,
    }
    return render(request, 'mainapp/product.html', context=content)


def contact(request):
    login_form = ShopUserLoginForm()
    content = {
        'page_title': 'контакты',
        'login_form': login_form,
    }
    return render(request, 'mainapp/contact.html', context=content)
