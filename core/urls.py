from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    path("admin-dashboard/", views.admin_dashboard_view, name="admin_dashboard"), 
    path("user-dashboard/", views.user_dashboard_view, name="user_dashboard"), 
    path("admin-users/", views.admin_users, name="admin_users"), 
    path("admin-settings/", views.admin_settings, name="admin_settings"), 
    path('toggle_user_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path("admin-categories/", views.admin_categories, name="admin_categories"), 
    path("add-category/", views.add_category, name="add_category"), 
    path("store-category/", views.store_category, name="store_category"), 
    path('category/edit/<int:pk>/', views.edit_category, name='edit_category'),
]