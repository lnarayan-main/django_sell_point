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


