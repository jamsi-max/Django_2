from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from mainapp.models import Product, ProductCategory
from basketapp.models import Basket
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.conf import settings

@login_required
def index(request):
    content = {
        'page_title': 'basket',
        'basket': request.user.basket.select_related('product__category').order_by('-product__price'),
        'mediaURL': settings.MEDIA_URL,
    }
    return render(request, 'basketapp/basket.html', context=content)


def add(request, pk):
    if request.is_ajax():
        if not request.user.is_authenticated:
            return JsonResponse({'result': 0})
        else:
            product = get_object_or_404(Product, pk=int(pk))
            basket_item = request.user.basket.filter(product=product).first()

            if not basket_item:
                basket_item = Basket(user=request.user, product=product)
            
            basket_item.quantity += 1
            basket_item.save()

            content = {
                'basket': request.user.basket.order_by('-product__price'),
                'mediaURL': settings.MEDIA_URL,
            }
            result = render_to_string('includes/inc__basket_view.html', context=content)

            return JsonResponse({'result': result})


@login_required
def remove(request, pk):
    get_object_or_404(Basket, pk=pk).delete()
    return HttpResponseRedirect(reverse('basket:index'))


@login_required
def update(request, pk, quantity):
    if request.is_ajax():
        item = get_object_or_404(Basket, pk=int(pk))
        if int(quantity) > 0:
            item.quantity = int(quantity)
            item.save()
        else:
            item.delete()

        content = {
            'basket': request.user.basket.select_related('product__category').order_by('-product__price'),
            'mediaURL': settings.MEDIA_URL,
        }

        result = render_to_string('includes/inc__basket_list.html', context=content)
        return JsonResponse({'result': result})


        
