from django.http import JsonResponse
from django.shortcuts import render
from core.decorators import admin_required, logged_in_required
from homepage.models import Category
from products.models import Favorite, Product, CartItem
from itertools import zip_longest
from django.db.models import OuterRef, Exists, Value, BooleanField

def chunked(iterable, n):
    args = [iter(iterable)] * n
    return zip_longest(*args)

# Create your views here.

# @logged_in_required
# @admin_required
def home(request):
    categories = Category.objects.all()
    user = request.user

    if user.is_authenticated:
        favorites = Favorite.objects.filter(user=user, product=OuterRef('pk'))
        cart_items = CartItem.objects.filter(user=user, product=OuterRef('pk'))

        products = Product.objects.annotate(
            is_favorited=Exists(favorites),
            is_carted=Exists(cart_items)
        )
    else:
        products = Product.objects.annotate(
            is_favorited=Value(False, output_field=BooleanField()),
            is_carted=Value(False, output_field=BooleanField())
        )

    grouped = list(chunked(products, 3))  # groups of 3 products per row

    context = {
        'categories': categories,
        'products': products,
        'grouped_products': grouped,
    }
    return render(request, 'homepage/home.html', context)

def register(request):
    return render(request, 'homepage/register.html')

def storeUser(request):
    print(request)


def shop_grid(request):
    return render(request, 'homepage/home/shop-grid.html')

def blog(request):
    return render(request, 'homepage/home/blog.html')

def contact(request):
    return render(request, 'homepage/home/contact.html')


def shoppingCart(request):
    cart_items = CartItem.objects.select_related('product').filter(user=request.user)
    total_items = cart_items.count()
    total_price = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'total_price': total_price,
    }
    return render(request, 'homepage/home/shoping-cart.html', context)


def update_cart_quantity(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = int(request.POST.get('quantity'))

        try:
            item = CartItem.objects.get(id=cart_item_id, user=request.user)
            item.quantity = quantity
            item.save()

            # Recalculate totals
            item_total = item.total_price
            total_price = sum(i.total_price for i in CartItem.objects.filter(user=request.user))

            return JsonResponse({
                'status': 'success',
                'message': 'Quantity updated',
                'item_total': f"{item_total:.2f}",
                'total_price': f"{total_price:.2f}"
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})



def remove_from_cart(request):
    if request.method == "POST" and request.user.is_authenticated:
        cart_item_id = request.POST.get('cart_item_id')
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
            cart_item.delete()

            # Calculate updated total
            cart_items = CartItem.objects.filter(user=request.user)
            total_price = sum(item.product.price * item.quantity for item in cart_items)

            return JsonResponse({'status': 'success', 'message': 'Item removed from Cart', 'total_price': total_price})
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

