from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


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
    users = User.objects.exclude(groups__name='admin')
    return render(request, 'homepage/admin/users-listing.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def admin_settings(request):
    users = User.objects.exclude(groups__name='user')
    return render(request, 'homepage/admin/settings.html', {'users': users})

