from django.urls import path
from . import views

urlpatterns = [
    path('my-products/', views.product_list, name='user_products'),
    path('products/create/', views.product_create, name='product_create'),
    path('product/update/<int:product_id>/', views.product_update, name='product_update'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/delete/<slug:slug>/', views.product_delete, name='product_delete'),
    path('product/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('product/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('product/<int:pk>/product-details', views.product_detail_page, name='product_detail_page'),
]