from django.shortcuts import render
from user_info.models import Users


# Create your views here.

def user_login(request):
    """
    用户登录视图函数,todo
    :param request: 需要获取,用户名和密码
    :return:
    """
    Users.objects.create(user_password="123456", user_telphone="131568955", user_gender=0)
    return render(request, "shop/login.html")


def register(request):
    """
    用户注册函数,todo
    :param request: 需要获取手机号码,密码
    :return:
    """
    return render(request, "shop/reg.html")
