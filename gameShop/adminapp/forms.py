from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory, News
from adminapp.utils import FormWidgetMixin, AgeValidationMixin


class AdminCreateUserForm(FormWidgetMixin, UserCreationForm, AgeValidationMixin):
    class Meta:
        model = ShopUser
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'age', 'email', 'avatar','is_staff', 'is_superuser', 'is_active')

    class_all_fields = 'form-item-news-add'
    

class AdminUpdateUserForm(FormWidgetMixin, UserChangeForm, AgeValidationMixin):
    class Meta:
        model = ShopUser
        fields = ('username', 'password', 'first_name', 'last_name', 'age', 'email', 'avatar', 'is_staff', 'is_superuser', 'is_active')

    class_all_fields = 'form-item-news-add'
    password = False


class AdminCreateCategoryForm(FormWidgetMixin, forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description', 'is_active')

    class_all_fields = 'form-item-news-add'


class AdminNewsAddForm(FormWidgetMixin, forms.ModelForm):
    class Meta:
        model = News
        fields = ('news_tite', 'news_content')

    class_all_fields = 'form-item-news-add'


class AdminCreateProductForm(FormWidgetMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'desc', 'desc_long', 'price', 'quantity', 'discount', 'is_active', 'image', 'alt')

    class_all_fields = 'form-item-news-add'



    
  

