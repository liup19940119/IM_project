from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View

from .forms import MyUserForm
from .models import MyUser, Contact


def register_user(request):
    username = request.GET['username']
    password = request.GET['password']
    mobile = request.GET['mobile']
    sex = request.GET['sex']

    if MyUser.objects.filter(Q(mobile=mobile) | Q(username=username)):
        return JsonResponse({'code': 1001, 'error_message': 'You have already registered'})

    else:
        try:
            user = MyUser()
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

    if not MyUser.objects.get(username=add_name):
        return JsonResponse({'code': 4002, 'message': '该用户不存在'})

    else:
        u = MyUser.objects.get(username=add_name)
        try:
            if Contact.objects.get(user=username, contacts=u):
                return JsonResponse({'code': 4003, 'message': '该用户已经是你的好友', 'add_name': add_name})
        except:
            c = Contact()
            c.user = username
            c.contacts = u
            c.save()

            return JsonResponse({'code': 4001, 'message': '添加成功', 'add_name': add_name})


class ShowInfo(View):
    def get(self, requset):
        username = requset.GET['username']
        try:
            u = MyUser.objects.get(username=username)
            return render(requset, 'show_info.html', {'info': u})
        except:
            pass


class WebRegister(View):
    def get(self, request):
        return render(request, 'register.html', {'form': MyUserForm().as_table(), 'value': ''})

    def post(self, request):
        myuserform = MyUserForm(request.POST, request.FILES)
        if myuserform.is_valid():
            username = myuserform.cleaned_data['username']
            mobile = myuserform.cleaned_data['mobile']
            u = MyUser()
            u.username = username
            u.password = myuserform.cleaned_data['password']
            u.sex = myuserform.cleaned_data['sex']
            u.email = myuserform.cleaned_data['email']
            u.mobile = mobile
            u.avatar = myuserform.cleaned_data['avatar']
            u.save()
            return render(request, 'register.html', {'value': 1002})

        return render(request, 'register.html', {'value': 1001})




