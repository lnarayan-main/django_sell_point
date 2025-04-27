from django import forms
from .models import Product, ProductImage, Category

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category")
    # ... other fields ...

    class Meta:
        model = Product
        fields = ['title', 'description', 'category', 'status', 'price', 'quantity']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_main']

ProductImageFormSet = forms.inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=3,
    can_delete=True
)