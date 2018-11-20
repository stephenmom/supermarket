from django.shortcuts import render, redirect, reverse
from django.views import View
from db.base_view import BaseVerifyView
from myrandom import random_user_info
from user_info.models import Users


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
        print(oneuser)
        if oneuser:
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
        return redirect(reverse("user_info:login"))
