from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from .models import User


def register_user(request):
    username = request.GET['username']
    password = request.GET['password']
    mobile = request.GET['mobile']
    sex = request.GET['sex']

    if User.objects.filter(Q(mobile=mobile) | Q(username=username)):
        return JsonResponse({'code': 1001, 'error_message': 'You have already registered'})

    else:
        try:
            user = User()
            user.username = username
            user.password = password
            user.mobile = mobile
            user.sex = sex
            user.save()

            return JsonResponse({'code': 1002, 'error_message': 'Register successed'})

        except:
            return JsonResponse({'code': 1003, 'error_message': 'Register failure, Please try again!!'})




