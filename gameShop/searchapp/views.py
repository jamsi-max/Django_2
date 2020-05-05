from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.conf import settings
from mainapp.models import Product

def search(request):
    if request.is_ajax():

        content = {
                'search_list': Product.objects.filter(name__icontains=request.GET['data']),
                'mediaURL': settings.MEDIA_URL,
            }
        result = render_to_string('includes/inc__search_list.html', context=content)

        return JsonResponse({'result': result})


