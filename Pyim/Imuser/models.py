import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils.timezone import now


class MyUser(AbstractUser):
    username = models.CharField(max_length=100, null=False, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=50, null=False, verbose_name='密码')
    mobile = models.CharField(unique=True, max_length=50, verbose_name='手机号')
    sex = models.CharField(max_length=50, null=False, verbose_name='性别')
    registerTime = models.DateTimeField(default=now)
    avatar = models.ImageField(verbose_name='头像')

    class Meta:
        db_table = 'user'
        ordering = ['username', 'registerTime']
        verbose_name = '用户'


class Contact(models.Model):
    user = models.CharField(max_length=100, null=False)
    contacts = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'contact'
        ordering = ['user']



