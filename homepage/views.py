from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'homepage/home.html')

def register(request):
    return render(request, 'homepage/register.html')

def storeUser(request):
    print(request)
