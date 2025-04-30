from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile-update/', views.user_profile_update, name='user_profile_update'),
]