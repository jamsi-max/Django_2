from django.urls import path, re_path

import searchapp.views as searchapp

app_name = 'searchapp'

urlpatterns = [
    re_path(r'^$', searchapp.search, name='search'),
]