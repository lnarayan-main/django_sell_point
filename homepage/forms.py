from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select Category",
        label="Parent Category"
    )
    status = forms.BooleanField(
        required=False,
        label="Status",
        initial=True,
        widget=forms.Select(choices=[(True, 'Active'), (False, 'Inactive')])
    )
    image = forms.ImageField(required=False)

    class Meta:
        model = Category
        fields = ['name', 'parent', 'status', 'image']