from django.shortcuts import render
from core.decorators import admin_required, logged_in_required

# Create your views here.

# @logged_in_required
# @admin_required
def home(request):
    return render(request, 'homepage/home.html')

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


