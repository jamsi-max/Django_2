from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms

from authapp.models import ShopUser
from mainapp.models import ProductCategory
from adminapp.utils import FormWidgetMixin, AgeValidationMixin


class ShopUserLoginForm(FormWidgetMixin, AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-log-item'})
        # }

    placeholder = True
    class_all_fields = 'form-log-item'


class ShopUserRegisterForm(FormWidgetMixin, UserCreationForm, AgeValidationMixin):
    class Meta:
        model = ShopUser
        fields = ('username', 'password1', 'password2', 'first_name', 'age', 'email', 'avatar')

    class_all_fields = 'form-reg-item'
    
    
class ShopUserEditForm(FormWidgetMixin, UserChangeForm, AgeValidationMixin):
    class Meta:
        model = ShopUser
        fields = ('username', 'password', 'first_name', 'age', 'email', 'avatar')

    class_all_fields = 'form-reg-item'
    password = False
     

class ShopUserChangePassword(FormWidgetMixin, PasswordChangeForm):
    class Meta:
        model = ShopUser
        fields = ('__all__')

    class_all_fields = 'form-reg-item'

 