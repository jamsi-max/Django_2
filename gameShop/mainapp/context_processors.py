def basket(request):
    return {'basket': request.user.basket.select_related('product__category').all()} if request.user.is_authenticated else {'basket': []}
