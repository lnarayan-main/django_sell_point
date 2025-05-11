from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop-grid/', views.shop_grid, name='shop_grid'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('shopping-cart/', views.shoppingCart, name='shopping-cart'),

]