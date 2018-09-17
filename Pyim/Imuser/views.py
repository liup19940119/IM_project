from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from .models import User, Contact


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


def add_user(requset):
    username = requset.GET['username']
    add_name = requset.GET['add_name']

    if not User.objects.get(username=add_name):
        return JsonResponse({'code': 4002, 'message': '该用户不存在'})

    else:
        u = User.objects.get(username=add_name)
        try:
            if Contact.objects.get(user=username, contacts=u):
                return JsonResponse({'code': 4003, 'message': '该用户已经是你的好友', 'add_name': add_name})
        except:
            c = Contact()
            c.user = username
            c.contacts = u
            c.save()

            return JsonResponse({'code': 4001, 'message': '添加成功', 'add_name': add_name})






