import random
import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views import View
from db.base_view import BaseVerifyView
from myrandom import random_user_info
from user_info.helper import send_sms
from user_info.models import Users, UserAddress
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


class Address(BaseVerifyView):
    """
    用户地址
    """

    # 用户地址
    # 第一步渲染静态页面
    # 第二步获取用户填写的地址详情,
    # 第三步保存用户的地址详情

    def get(self, request):
        tellphone = request.session.get("tellphone")
        user = Users.objects.get(user_telphone=tellphone)
        addrs = UserAddress.objects.filter(user_id=user)
        context = {
            "addrs": addrs
        }
        return render(request, "shop/gladdress.html", context)

    def post(self, request):
        return redirect(reverse("user_info:login"))


class AddressAdd(BaseVerifyView):
    """
    添加用户地址
    """

    # 用户地址
    # 第一步渲染静态页面
    # 第二步获取用户填写的地址详情,
    # 第三步保存用户的地址详情

    def get(self, request):
        context = {

        }
        return render(request, "shop/address.html", context)

    def post(self, request):
        tellphone = request.session.get("tellphone")
        user = Users.objects.get(user_telphone=tellphone)
        hcity = request.POST.get("hcity")
        hproper = request.POST.get("hproper")
        harea = request.POST.get("harea")
        address_detail = request.POST.get("address_detail")
        consignee_name = request.POST.get("consignee_name")
        consignee_phone = request.POST.get("consignee_phone")
        isdefault = False
        if request.POST.get("isdefault"):
            UserAddress.objects.filter(user_id=user).update(default_address=False)
            isdefault = True
        UserAddress.objects.create(user_id=user,
                                   goods_user_name=consignee_name,
                                   goods_user_phone=consignee_phone,
                                   goods_detail=address_detail,
                                   default_address=isdefault,
                                   province_id=hcity,
                                   city_id=hproper,
                                   district_id=harea, )

        return redirect(reverse("user_info:address"))


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
        user = Users.objects.get(user_telphone=tellphone)
        if request.FILES.get("user_head"):
            user.user_head = request.FILES.get("user_head")
        user.user_name = request.POST.get("nickname")
        user.user_gender = request.POST.get("gender")
        user.user_brith = request.POST.get("birth_of_date")
        user.user_school = request.POST.get("school")
        user.user_address = request.POST.get("address")
        user.user_hometown = request.POST.get("hometown")
        user.save()
        return redirect("user_info:info")


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
        #####################################################################
        # __business_id = uuid.uuid1()
        # params = "{\"code\":\"%s\",\"product\":\"天气不错\"}" % random_code
        # print(send_sms(__business_id, phone, "注册验证", "SMS_2245271", params))
        #####################################################################
        return JsonResponse({"err": 0})
    else:
        # 提示请求方式错误 json 格式
        return JsonResponse({"err": 1, "errmsg": "请求方式错误!"})
