from django.urls import path
from . import views

urlpatterns = [
    path('my-products/', views.product_list, name='user_products'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/delete/<slug:slug>/', views.product_delete, name='product_delete'),
]