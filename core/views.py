from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from homepage.forms import CategoryForm
from homepage.models import Category
from django.urls import reverse
from django.contrib import messages


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user role
                if user.groups.filter(name="admin").exists() or user.is_superuser:
                    return redirect("admin_dashboard")  # Redirect to admin dashboard
                elif user.groups.filter(name="user").exists():
                    return redirect("user_dashboard")  # Redirect to user dashboard
                else:
                    return redirect("home")  # Fallback redirection
        else:
            # Form is invalid, show errors
            return render(request, "core/login.html", {"form": form})
    else:
        form = AuthenticationForm()
    return render(request, "core/login.html", {"form": form})


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_group = Group.objects.get(name='user')
            user.groups.add(user_group)
            login(request, user)
            return redirect("user_dashboard")  # Redirect to user dashboard
        else:
            return render(request, "core/register.html", {"form": form})
    else:
        form = UserRegistrationForm()
    return render(request, "core/register.html", {"form": form})

def is_admin(user):
    return user.groups.filter(name='admin').exists() or user.is_superuser

def is_regular_user(user):
    return user.groups.filter(name='user').exists()

@login_required
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    return render(request, 'homepage/admin_dashboard.html')

@login_required
@user_passes_test(is_regular_user)
def user_dashboard_view(request):
    return render(request, 'homepage/user_dashboard.html')

@login_required
@user_passes_test(is_admin)
def admin_users(request):
    # users = User.objects.all()
    query = request.GET.get('q')  # Get the search query from the request
    if query:
        query = query.strip()
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        ).exclude(groups__name='admin')
    else:
        users = User.objects.exclude(groups__name='admin')

    paginator = Paginator(users, 10)  # Show 10 categories per page
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    context = {
        'users': users,
        'search_query': query,
    }

    return render(request, 'homepage/admin/users-listing.html', context)

@login_required
@user_passes_test(is_admin)
def admin_settings(request):
    users = User.objects.exclude(groups__name='user')
    return render(request, 'homepage/admin/settings.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def toggle_user_status(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        user.is_active = not user.is_active
        user.save()
        return JsonResponse({'status': 'success', 'new_status': user.is_active})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
    

@login_required
@user_passes_test(is_admin)
def admin_categories(request):
    query = request.GET.get('q')
    categories_list = Category.objects.all().order_by('-created_at')

    if query:
        query = query.strip()
        categories_list = Category.objects.filter(
            Q(name__icontains=query)
        ).order_by('-created_at')

    paginator = Paginator(categories_list, 10)  # Show 10 categories per page
    page = request.GET.get('page')

    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'search_query': query,
    }
    return render(request, 'homepage/admin/categories-listing.html', context)


@login_required
@user_passes_test(is_admin)
def add_category(request):
    form = CategoryForm()
    context = {'form': form}
    return render(request, 'homepage/admin/categories-add.html', context)

@login_required
@user_passes_test(is_admin)
def store_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect(reverse('admin_categories'))  # Redirect to the category list view
        else:
            messages.error(request, 'There was an error creating the category. Please correct the form.')
            context = {'form': form}
            return render(request, 'homepage/admin/categories-add.html', context)
    else:
        # If someone tries to access the store URL with a GET request
        return redirect(reverse('add_category'))
    
@login_required
@user_passes_test(is_admin)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)  # Get the category or return a 404 error
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)  # Populate the form with existing category data
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect(reverse('admin_categories'))  # Redirect to the category list view
        else:
            messages.error(request, 'There was an error updating the category. Please correct the form.')
    else:
        form = CategoryForm(instance=category)  # Populate the form with existing category data
    context = {
        'form': form,
        'category': category,  # Pass the category object to the template
    }
    return render(request, 'homepage/admin/categories-edit.html', context)


@login_required
@user_passes_test(is_admin)
def toggle_category_status(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=category_id)
        category.status = not category.status
        category.save()
        return JsonResponse({'status': 'success', 'new_status': category.status})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)