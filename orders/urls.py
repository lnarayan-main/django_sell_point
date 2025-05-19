from django.urls import path
from . import views

urlpatterns = [
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
]