from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
import random, hashlib

from authapp.models import ShopUser, ShopUserProfile
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

    def save(self, commit=True):
        user = super().save()

        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()

        return user
    
    
class ShopUserEditForm(FormWidgetMixin, UserChangeForm, AgeValidationMixin):
    class Meta:
        model = ShopUser
        fields = ('username', 'password', 'first_name', 'age', 'email', 'avatar')

    class_all_fields = 'form-reg-item'
    password = False


class ShopUserProfileEditForm(FormWidgetMixin, forms.ModelForm, AgeValidationMixin):
    class Meta:
        model = ShopUserProfile
        exclude = ('user',)

    class_all_fields = 'form-reg-item'
    password = False
     

class ShopUserChangePassword(FormWidgetMixin, PasswordChangeForm):
    class Meta:
        model = ShopUser
        fields = ('__all__')

    class_all_fields = 'form-reg-item'

 