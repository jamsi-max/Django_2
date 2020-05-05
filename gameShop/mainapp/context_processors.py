def basket(request):
    return {'basket': request.user.basket.all()} if request.user.is_authenticated else {'basket': []}