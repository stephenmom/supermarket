from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
from django_redis import get_redis_connection

from db.base_view import BaseVerifyView
from product.models import ProSKU
from user_info.models import UserAddress, Users


class MaKeOrder(BaseVerifyView):
    def get(self, request):
        tellphone = request.session.get("tellphone")
        user = Users.objects.get(user_telphone=tellphone)
        addr = UserAddress.objects.filter(user_id=user, default_address=True).first()
        if not addr:
            addr = UserAddress.objects.filter(user_id=user).first()

        conn = get_redis_connection("default")
        cart_key = 'card_%d' % user.pk
        cart_dict = conn.hgetall(cart_key)
        skus = []
        for sku_id, count in cart_dict.items():
            sku = ProSKU.objects.get(pk=sku_id)
            sku.count = count
            skus.append(sku)
        context = {
            "addr": addr,
            "skus": skus
        }
        return render(request, "shop/tureorder.html", context)

    def post(self, request):
        tellphone = request.session.get("tellphone")
        if not tellphone:
            return JsonResponse({"res": -1, "errmsg": "没有登录"})
        user = Users.objects.get(user_telphone=tellphone)
        sku_id = request.POST.get("sku_id")
        conn = get_redis_connection("default")
        cart_key = 'card_%d' % user.pk
        if sku_id == "":
            return JsonResponse({"res": 2, "error": "失败,不能为空选"})
        li1 = sku_id.split("|")
        li2 = []
        for v in li1:
            li2.append(conn.hget(cart_key, v))
        print([int(x) for x in li2])
        return JsonResponse({"res": 3, "error": "成功"})
