from django.shortcuts import render
from core.decorators import admin_required, logged_in_required
from homepage.models import Category
from products.models import Product
from itertools import zip_longest

def chunked(iterable, n):
    args = [iter(iterable)] * n
    return zip_longest(*args)

# Create your views here.

# @logged_in_required
# @admin_required
def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    grouped = list(chunked(products, 3))  
    context = {
        'categories' : categories,
        'products' : products,
        'grouped_products' : grouped
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


