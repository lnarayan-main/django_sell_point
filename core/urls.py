from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),
]