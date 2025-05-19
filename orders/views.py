from django.shortcuts import render, redirect
from orders.models import Order, OrderItem, Payment
import stripe
from django.conf import settings

from products.models import CartItem

stripe.api_key = settings.STRIPE_SECRET_KEY

def order_success(request):
    payment_intent_id = request.POST.get('payment_intent')
    if not payment_intent_id:
        return redirect('shopping-cart')

    intent = stripe.PaymentIntent.retrieve(payment_intent_id)

    # Create Order
    order = Order.objects.create(
        user=request.user,
        full_name=request.user.get_full_name(),
        email=request.user.email,
        total_amount=intent.amount / 100,
        is_paid=True,
        address=request.POST.get('address'),
        city=request.POST.get('city'),
        state=request.POST.get('state'),
        zipcode=request.POST.get('zipcode'),
        phone=request.POST.get('phone_number'),
    )

    # Create OrderItems from cart
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # Create Payment
    Payment.objects.create(
        order=order,
        payment_intent=payment_intent_id,
        amount=intent.amount / 100,
        payment_status=intent.status,
        payment_method=intent.payment_method_types[0]
    )

    # Clear cart
    cart_items.delete()
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')

    return render(request, 'homepage/home/order_success.html', {'orders': orders})


def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    return render(request, 'homepage/home/order_success.html', {'orders': orders})