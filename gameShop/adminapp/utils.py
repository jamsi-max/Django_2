from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect
from django import forms

from django.views.generic.edit import DeleteView



class SuperuserCheckMixin:
    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class SoftDeleteMixin(DeleteView):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        return HttpResponseRedirect(self.get_success_url())
    

class TitleMixin:
    title = ''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.title
        return context

class FormWidgetMixin:
    class_all_fields = None
    placeholder = False
    password = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = self.class_all_fields
            field.help_text = ''
            if not self.password and field_name == 'password':
                field.widget = forms.HiddenInput()
            if self.placeholder:
                field.widget.attrs['placeholder'] = f'{field_name}'


class AgeValidationMixin:
    def clean_age(self):
            age = self.cleaned_data['age']
            if age < 18:
                raise forms.ValidationError(f'You must be over 18 years old')
            return age


def togle_active(odj):
        if odj.is_active:
            odj.is_active = False
        else:
            odj.is_active = True
        odj.save()

