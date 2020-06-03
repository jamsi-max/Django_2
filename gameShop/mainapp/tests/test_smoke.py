from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory
from django.core.management import call_command
from django.shortcuts import reverse

class TestMainappSmoke(TestCase):

    fixtures = ['mainapp.json']

    def setUp(self):     
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/6/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/category/0/1/')
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(reverse('products:category', kwargs={'pk': category.pk, 'page': 1}))
            self.assertEqual(response.status_code, 200)

        for product in Product.objects.all():
            response = self.client.get(reverse('products:product', kwargs={'pk': product.pk}))

            self.assertEqual(response.status_code, 200)
