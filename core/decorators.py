# your_app/decorators.py
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from functools import wraps
from django.contrib.auth.decorators import login_required
from .utils import is_admin, is_regular_user  # Import your utility functions


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if is_admin(request.user):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You do not have permission to access this page.")
            return redirect(reverse('home'))  # Adjust redirect URL as needed
    return _wrapped_view


def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if is_regular_user(request.user):
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "This page is for regular users only.")
            return redirect(reverse('home'))  # Adjust redirect URL as needed
    return _wrapped_view


# Example of a decorator for both logged-in users (can be admin or regular)
def logged_in_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You need to be logged in to access this page.")
            return redirect('login')  # Adjust redirect URL as needed
            # return redirect(reverse('login'))  # Adjust redirect URL as needed
    return _wrapped_view