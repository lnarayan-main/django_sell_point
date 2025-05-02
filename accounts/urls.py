from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/update-pic/', views.update_pic, name='update_pic'),
    path('profile-update/', views.user_profile_update, name='user_profile_update'),
]
