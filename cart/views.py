from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from django_redis import get_redis_connection
from db.base_view import BaseVerifyView
from product.models import ProSKU
from user_info.models import Users


# Create your views here.
class CartAdd(View):
    def get(self, request):

        return JsonResponse({"res": "get方法", "errmsg": "get方法"})

    def post(self, request):
        """
               购物车记录添加
               :param request:
               :return: json数据
               """
        # 接收数据
        # 数据校验
        # 添加购物车记录
        # 返回一个应答
        tellphone = request.session.get("tellphone")
        if not tellphone:
            return JsonResponse({"res": -1, "errmsg": "没有登录"})
        user = Users.objects.get(user_telphone=tellphone)
        sku_id = request.POST.get("sku_id")
        count = request.POST.get("count")
        if not all([sku_id, count]):
            return JsonResponse({"res": 0, "errmsg": "数据不完整"})
        # 如果传入的count不是数字怎么办
        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({"res": 1, "errmsg": "数目出错"})

        # 判断商品是否存在
        sku = ProSKU.objects.filter(pk=sku_id).first()
        if not sku:
            return JsonResponse({"res": 2, "errmsg": "商品不存在"})

        # 添加购物车记录

        conn = get_redis_connection("default")
        cart_key = 'card_%d' % user.pk
        cart_count = conn.hget(cart_key, sku_id)
        if cart_count:
            count += int(cart_count)
        conn.hset(cart_key, sku_id, count)
        return JsonResponse({"res": 4, "errmsg": "添加成功"})


class CartChange(View):
    def get(self, request):

        return JsonResponse({"res": "get方法", "errmsg": "get方法"})

    def post(self, request):
        tellphone = request.session.get("tellphone")
        if not tellphone:
            return JsonResponse({"res": -1, "errmsg": "没有登录"})
        user = Users.objects.get(user_telphone=tellphone)
        sku_id = request.POST.get("sku_id")
        if not sku_id:
            return JsonResponse({"res": 0, "errmsg": "数据不完整"})

        # 判断商品是否存在
        sku = ProSKU.objects.filter(pk=sku_id).first()
        if not sku:
            return JsonResponse({"res": 2, "errmsg": "商品不存在"})

        # 删除购物车记录
        conn = get_redis_connection("default")
        cart_key = 'card_%d' % user.pk
        conn.hdel(cart_key, sku_id)
        return JsonResponse({"res": 4, "errmsg": "删除成功"})


class CartInfo(BaseVerifyView):
    def get(self, request):
        tellphone = request.session.get("tellphone")
        user = Users.objects.get(user_telphone=tellphone)
        conn = get_redis_connection("default")
        cart_key = 'card_%d' % user.pk
        cart_dict = conn.hgetall(cart_key)
        skus = []
        for sku_id, count in cart_dict.items():
            sku = ProSKU.objects.get(pk=sku_id)
            sku.count = count
            skus.append(sku)
        context = {
            "skus": skus
        }
        return render(request, "shop/shopcart.html", context)

    def post(self, reuqest):
        pass


class Cart(View):
    def get(self, request):
        context = {

        }
        return redirect("cart:cart_info")

    def post(self, request):
        context = {

        }
        return render(request, "shop/shopcart.html", context)

