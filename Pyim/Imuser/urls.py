from django.urls import path

from .views import register_user, add_user

urlpatterns = [
    path('register/', register_user, name='register'),
    path('add_user', add_user, name='add_user'),
]