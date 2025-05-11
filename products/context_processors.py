from .models import CartItem, Favorite

def favorite_count(request):
    if request.user.is_authenticated:
        count = Favorite.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'favorite_count': count}

def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    return {'cart_count': count}
