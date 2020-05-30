from django.db import models
from django.shortcuts import reverse

from adminapp.utils import togle_active


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=64, unique=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    is_active = models.BooleanField(verbose_name='Активна', default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category', kwargs={'pk': self.pk, 'page': 1})

    def soft_delete(self):
        togle_active(self)

    class Meta:
        ordering = ['-is_active', 'name']  

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя продукта', max_length=128, unique=True)
    desc = models.CharField(verbose_name='краткое описание продукта', max_length=128)
    desc_long = models.TextField(verbose_name='описание продукта', blank=True)
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2, default=0)
    image = models.ImageField(upload_to="products_images", blank=True, default='no-image.jpg')
    alt = models.CharField(verbose_name='короткое имя продукта', max_length=64, blank=True)
    quantity = models.PositiveIntegerField(verbose_name='количество товара', default=0)
    discount = models.PositiveIntegerField(verbose_name='скидка на товара', default=0)
    is_active = models.BooleanField(verbose_name='удален', default=True, db_index=True)
    created_at = models.DateTimeField(verbose_name='дата добавления товара', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='дата изменения карточки товара', auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.category})"
    
    @classmethod
    def get_items(cls):
        return cls.objects.filter(is_active=True)

    def get_absolute_url(self):
        return reverse('products:product', kwargs={'pk': self.pk}) 
    
    @property
    def get_discount_price(self):
        return float(self.price) - (float(self.price) * (self.discount / 100))

    def soft_delete(self):
        togle_active(self)
    
    class Meta:
        ordering = ['-is_active', 'name'] 

class MainSocial(models.Model):
    name = models.CharField(verbose_name='имя социальной сети', max_length=24, unique=True)
    href = models.CharField(verbose_name='ccылкана страницу социальной сети', max_length=128, default='#')
    image = models.ImageField(upload_to="products_images", blank=True)
    alt = models.CharField(verbose_name='короткое имя', max_length=24, unique=True)

    def __str__(self):
        return self.name

class Services(models.Model):
    title = models.CharField(verbose_name='имя сервиса', max_length=64, unique=True)
    content = models.TextField(verbose_name='описание сервиса')
    image = models.ImageField(upload_to="products_images")

    def __str__(self):
        return self.title

class News(models.Model):
    data = models.DateTimeField(verbose_name='дата добавления новости', auto_now_add=True)
    news_tite = models.CharField(verbose_name='заголовок новости', max_length=64, unique=True)
    news_content = models.TextField(verbose_name='содержание статьи')
    is_active = models.BooleanField(verbose_name='удален', default=True)

    def __str__(self):
        return self.news_tite

    def get_absolute_url(self):
        return reverse('news', kwargs={'pk': self.pk})

    def soft_delete(self):
        togle_active(self)

    class Meta:
        ordering = ['-is_active', '-data'] 

class Team(models.Model):
    name = models.CharField(verbose_name='имя', max_length=32)
    post = models.CharField(verbose_name='должность', max_length=32)
    image = models.ImageField(upload_to="products_images")

    def __str__(self):
        return self.name
    
    
