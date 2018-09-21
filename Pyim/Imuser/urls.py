from django.urls import path

from .views import register_user, add_user, ShowInfo, WebRegister

urlpatterns = [
    path('register/', register_user, name='register'),
    path('add_user', add_user, name='add_user'),
    path('show_info', ShowInfo.as_view(), name='show_info'),
    path('web_register/', WebRegister.as_view(), name='web_register')
]