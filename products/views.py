from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from .models import Favorite, Product, ProductImage, CartItem
from .forms import ProductForm, ProductImageFormSet
from django.http import JsonResponse
from django.urls import reverse

@login_required
def product_list(request):
    products = request.user.products.all()
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_create1(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        image_formset = ProductImageFormSet(request.POST, request.FILES, instance=Product(user=request.user))
        if product_form.is_valid() and image_formset.is_valid():
            print('form valid')
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()
            image_formset.instance = product
            image_formset.save()
            return redirect('user_products')
        else:
            print('form in-valid')
            return render(request, 'products/product_create.html', {
                'product_form': product_form,
                'image_formset': image_formset,
                'action': 'Create'
            })
    else:
        product_form = ProductForm()
        image_formset = ProductImageFormSet(instance=Product(user=request.user))
    return render(request, 'products/product_create.html', {
        'product_form': product_form,
        'image_formset': image_formset,
        'action': 'Create'
    })


@login_required
def product_create(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        image_formset = ProductImageFormSet(request.POST, request.FILES, instance=Product(user=request.user))
        if product_form.is_valid() and image_formset.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()
            image_formset.instance = product
            image_formset.save()
            #  Return a JSON response for AJAX
            return JsonResponse({
                'status': 'success',
                'message': 'Product created successfully!',
                'redirect': reverse('user_products') #  Include a redirect URL if needed
            })
        else:
            #  Return JSON error response
            errors = {}
            if product_form.errors:
                errors['product_form'] = product_form.errors
            if image_formset.errors:
                errors['image_formset'] = image_formset.errors
            return JsonResponse({
                'status': 'error',
                'message': 'Form validation failed',
                'errors': errors
            }, status=400)  #  Use a 400 Bad Request status code
    else:
        product_form = ProductForm()
        image_formset = ProductImageFormSet(instance=Product(user=request.user))
    return render(request, 'products/product_create.html', {
        'product_form': product_form,
        'image_formset': image_formset,
        'action': 'Create'
    })


@login_required
def product_update1(request, product_id):
    product = get_object_or_404(Product, pk=product_id, user=request.user)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        image_formset = ProductImageFormSet(request.POST, request.FILES, instance=product)

        if product_form.is_valid() and image_formset.is_valid():
            product = product_form.save()
            image_formset.save()
            return redirect('user_products')
        else:
            print("Form Errors:", product_form.errors)
            print("Image Formset Errors:", image_formset.errors)
            return render(request, 'products/product_create.html', {
                'product_form': product_form,
                'image_formset': image_formset,
                'action': 'Update'
            })
    else:
        product_form = ProductForm(instance=product)
        image_formset = ProductImageFormSet(instance=product)

    return render(request, 'products/product_create.html', {
        'product_form': product_form,
        'image_formset': image_formset,
        'action': 'Update'
    })

@login_required
def product_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id, user=request.user)  # Ensure user owns the product

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # instance=product for update
        if form.is_valid():
            form.save()
            #  Return a JSON response for AJAX
            return JsonResponse({
                'status': 'success',
                'message': 'Product updated successfully!',
                'redirect': reverse('user_products')  #  Include a redirect URL
            })
        else:
            #  Return JSON error response
            errors = {}
            if form.errors:
                errors['product_form'] = form.errors
            return JsonResponse({
                'status': 'error',
                'message': 'Form validation failed',
                'errors': errors
            }, status=400)  #  Use a 400 Bad Request status code
    else:
        product_form = ProductForm(instance=product)
        image_formset = ProductImageFormSet(instance=product)

    return render(request, 'products/product_create.html', {
        'product_form': product_form,
        'image_formset': image_formset,
        'action': 'Update'
    })





@login_required
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, user=request.user)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug, user=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('user_products')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


@login_required
def toggle_favorite(request):
    product_id = request.POST.get('product_id')
    user = request.user

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

    favorite, created = Favorite.objects.get_or_create(user=user, product=product)

    if not created:
        favorite.delete()
        count = Favorite.objects.filter(user=user).count()
        return JsonResponse({
            "status": "success",
            "message": "Removed from favorites",
            "is_favorited": False,
            "favorite_count": count
        })
    else:
        count = Favorite.objects.filter(user=user).count()
        return JsonResponse({
            "status": "success",
            "message": "Added to favorites",
            "is_favorited": True,
            "favorite_count": count
        })


@login_required
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))  # Default quantity is 1
    user = request.user

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

    cart_item, created = CartItem.objects.get_or_create(user=user, product=product)

    if not created:
        cart_item.quantity += quantity
        cart_item.save()
        message = 'Cart updated successfully'
    else:
        cart_item.quantity = quantity
        cart_item.save()
        message = 'Product added to cart'

    cart_count = CartItem.objects.filter(user=user).count()

    return JsonResponse({
        'status': 'success',
        'message': message,
        'cart_count': cart_count,
        'is_carted': True,
    })

def product_detail_page(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'homepage/home/product-details.html', {'product': product})