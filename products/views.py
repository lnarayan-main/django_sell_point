from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from .models import Product, ProductImage
from .forms import ProductForm, ProductImageFormSet

@login_required
def product_list(request):
    products = request.user.products.all()
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        image_formset = ProductImageFormSet(request.POST, request.FILES, instance=Product(user=request.user))
        if product_form.is_valid() and image_formset.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()
            image_formset.instance = product
            image_formset.save()
            return redirect('user_products')
    else:
        product_form = ProductForm()
        image_formset = ProductImageFormSet(instance=Product(user=request.user))
    return render(request, 'products/product_create.html', {'product_form': product_form, 'image_formset': image_formset, 'action': 'Create'})


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

# ... (update and delete views for Category can be added similarly)