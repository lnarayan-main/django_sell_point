from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop-grid/', views.shop_grid, name='shop_grid'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('shopping-cart/', views.shoppingCart, name='shopping-cart'),
    path('update-cart-quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('place-order/', views.place_order, name='place-order'),

]