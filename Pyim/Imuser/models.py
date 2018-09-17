import datetime

from django.db import models

# Create your models here.
from django.utils.timezone import now


class User(models.Model):
    username = models.CharField(max_length=100, null=False, unique=True)
    password = models.CharField(max_length=50, null=False)
    mobile = models.CharField(unique=True, max_length=50)
    sex = models.CharField(max_length=50, null=False)
    registerTime = models.DateTimeField(default=now)

    class Meta:
        db_table = 'user'
        ordering = ['username']
        verbose_name = '用户'


class Contact(models.Model):
    user = models.CharField(max_length=100, null=False)
    contacts = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'contact'
        ordering = ['user']



