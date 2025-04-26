from django.contrib.auth.models import User

def is_admin(user: User) -> bool:
    return user.is_authenticated and (user.groups.filter(name='admin').exists() or user.is_superuser)

def is_regular_user(user: User) -> bool:
    return user.is_authenticated and user.groups.filter(name='user').exists()