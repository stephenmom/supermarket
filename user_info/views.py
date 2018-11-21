import random
import uuid
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views import View
from db.base_view import BaseVerifyView
from myrandom import random_user_info
from user_info.helper import send_sms
from user_info.models import Users
import re
from django_redis import get_redis_connection


class UserLogin(View):
    def get(self, request):
        """
          用户登录get函数,todo
          :param request: 需要获取,用户名和密码
          :return:
        """
        login_error_context = {
        }
        return render(request, "shop/login.html", login_error_context)

    def post(self, request):
        tellphone = request.POST.get("tellphone")
        password = request.POST.get("password")
        oneuser = Users.objects.filter(user_password=password, user_telphone=tellphone).first()
        if oneuser:  # 如果登录成功
            request.session["tellphone"] = tellphone
            return redirect(reverse("user_info:member"))
        else:
            login_error_context = {
                "error": "login_fail",
            }
            return render(request, "shop/login.html", login_error_context)


class Register(View):
    def get(self, request):
        """
             用户注册get函数,todo
        """
        return render(request, "shop/reg.html")

    def post(self, request):
        """
               用户注册post函数,todo
        """
        tellphone = request.POST.get("tellphone")
        password = request.POST.get("password")
        Users.objects.create(user_password=password, user_telphone=tellphone, user_name="匿名" + random_user_info()[1])
        return redirect(reverse("user_info:login"))


class Forget(View):
    """
    忘记密码
    """

    def get(self, request):
        return render(request, "shop/forgetpassword.html")

    def post(self, request):
        return redirect(reverse("user_info:login"))


class Member(BaseVerifyView):
    """
    用户中心
    """

    def get(self, request):
        tellphone = request.session.get("tellphone")
        context = {
            "tellphone": tellphone
        }
        return render(request, "shop/member.html", context)

    def post(self, request):
        return redirect(reverse("user_info:login"))


class Logout(BaseVerifyView):
    """
    用户注销
    """

    def get(self, request):
        try:
            del request.session["tellphone"]
        except Exception as e:
            print(e)
        return redirect(reverse("user_info:login"))


class Info(BaseVerifyView):
    """
    用户个人资料
    """

    def get(self, request):
        tellphone = request.session.get("tellphone")
        user = Users.objects.filter(user_telphone=tellphone).first()
        context = {
            "user": user
        }
        return render(request, "shop/infor.html", context)

    def post(self, request):
        tellphone = request.session.get("tellphone")
        user = Users.objects.filter(user_telphone=tellphone).first()
        user.head = request.FILES['user_head']
        user.save()
        # return redirect(reverse("user_info:info"))
        context = {
            "user": user
        }
        return render(request, "shop/infor.html", context)


def send_msg_phone(request):
    """发生短信的视图函数"""
    if request.method == "POST":
        # 接收到手机号码
        phone = request.POST.get("phone", "")
        # 后端验证手机号码格式是否正确
        # 创建正则对象
        phone_re = re.compile("^1[3-9]\d{9}$")
        # 匹配传入的手机号码
        rs = re.search(phone_re, phone)
        if rs is None:
            # 手机号码格式错误
            return JsonResponse({"err": 1, "errmsg": "手机号码格式错误!"})
        # 生成随机码 随机数字组成
        random_code = "".join([str(random.randint(0, 9)) for _ in range(4)])

        # 保存随机码到redis中
        # 使用redis, 获取redis连接

        r = get_redis_connection("default")
        # 直接开始操作
        r.set(phone, random_code)
        # 设置过期时间
        r.expire(phone, 120)
        # 发送短信
        print(random_code)
        # 使用阿里发生短信
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\",\"product\":\"天气不错\"}" % random_code
        print(send_sms(__business_id, phone, "注册验证", "SMS_2245271", params))
        return JsonResponse({"err": 0})
    else:
        # 提示请求方式错误 json 格式
        return JsonResponse({"err": 1, "errmsg": "请求方式错误!"})
