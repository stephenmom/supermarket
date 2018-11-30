from alipay import AliPay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django_redis import get_redis_connection
from db.base_view import BaseVerifyView
from order.models import Transport, OrderGoods, OderInfo
from product.models import ProSKU
from user_info.models import UserAddress, Users
from datetime import datetime
import random
import os


# Create your views here.

class MaKeOrder(BaseVerifyView):
    def get(self, request):
        """
        下单操作
        :param request:
        :return:
        """
        # 获取用户的session手机号
        tellphone = request.session.get("tellphone")
        user = Users.objects.get(user_telphone=tellphone)
        # 获取默认收货地址
        addr = UserAddress.objects.filter(user_id=user, default_address=True).first()
        if not addr:
            addr = UserAddress.objects.filter(user_id=user).first()
        # 拿到redis连接
        conn = get_redis_connection("default")
        # 拼接redis里面cartkey的键
        cart_key = 'card_%d' % user.pk
        cart_dict = conn.hgetall(cart_key)
        # 购物车的选中过滤
        select_id = ""
        if request.GET.get("select_id"):
            select_id = request.GET.get("select_id")
        li1 = select_id.split("|")
        filter1 = [x for x in li1]
        # 获取商品以及商品的数量
        skus = []
        total_price = 0
        for sku_id, count in cart_dict.items():
            sku = ProSKU.objects.get(pk=sku_id)
            sku.count = count
            if str(sku.pk) in filter1:
                total_price += int(sku.count) * int(sku.pro_price)
                skus.append(sku)
        if not skus:
            return redirect("cart:cart_info")
        tr = Transport.objects.all().order_by("money")
        context = {
            "addr": addr,
            "skus": skus,
            "total_price": total_price,
            "transports": tr
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
        return JsonResponse({"res": 3, "error": "成功"})


class SubmitOrder(View):
    def get(self, request):
        pass

    def post(self, request):
        # 判断用户是否登录
        tellphone = request.session.get("tellphone")
        user = Users.objects.get(user_telphone=tellphone)
        if user is None:
            return JsonResponse({"code": 1, "errmsg": "没有登录!"})
        # 接收参数
        address_id = request.POST.get("address_id")
        sku_ids = request.POST.getlist("sku_id")
        transport = request.POST.get("transport")
        # 判断参数的合法性
        if not all([address_id, sku_ids, transport]):
            return JsonResponse({"code": 2, "errmsg": "参数错误!"})
        # 判断是否为整数
        try:
            address_id = int(address_id)
            transport = int(transport)
            sku_ids_int = [int(sku_id) for sku_id in sku_ids]
        except Exception as  e:
            return JsonResponse({"code": 3, "errmsg": "参数错误!"})

        # 判断收货地址和运输方式必须存在
        try:
            address = UserAddress.objects.get(pk=address_id, address_status=False)
        except UserAddress.DoesNotExist:
            return JsonResponse({"code": 4, "errmsg": "收货地址不存在!"})

        try:
            trans = Transport.objects.get(pk=transport, transport_status=False)
        except Transport.DoesNotExist:
            return JsonResponse({"code": 5, "errmsg": "运输方式不存在!"})

        # 保存数据到订单表中

        # 先保存订单基本信息表
        # 准备订单编号
        order_sn = "{}{}{}".format(datetime.now().strftime("%Y%m%d%H%M%S"), user.pk, random.randint(10000, 99999))
        # 准备详细地址
        address_detail = "{}{}{}-{}".format(address.province_id, address.city_id, address.district_id,
                                            address.goods_detail)

        # 返回的订单基本信息对象
        order = OderInfo.objects.create(
            order_number=order_sn,
            user_id=user,
            order_user_name=address.goods_user_name,
            order_user_phone=address.goods_user_phone,
            order_address=address_detail,
            order_transport=trans.name,
            order_transport_price=trans.money
        )

        # 连接redis
        r = get_redis_connection("default")
        # 准备key
        cart_key = 'card_%d' % user.pk

        # 先保存订单商品表
        # 准备个变量保存商品总价格
        order_amount = 0

        # 遍历商品的id
        for sku_id in sku_ids_int:
            # 保存商品到订单商品表
            # 保证商品也得存在
            try:
                goodssku = ProSKU.objects.get(pk=sku_id, pro_status=False, pro_show=True)
            except ProSKU.DoesNotExist:
                # 商品不存在
                return JsonResponse({"code": 6, "errmsg": "商品不存在!"})

            # 获取购物车中的数量
            count = r.hget(cart_key, sku_id)
            count = int(count)

            # 保证库存足够
            if goodssku.pro_inventory < count:
                return JsonResponse({"code": 7, "errmsg": "商品库存不足!"})

            # 保存订单商品表
            OrderGoods.objects.create(
                order=order,
                goods_sku=goodssku,
                price=goodssku.pro_price,
                count=count
            )

            # 销量增加
            goodssku.pro_sales_volume += count
            # 库存减少
            goodssku.pro_inventory -= count
            # 保存
            goodssku.save()

            # 统计总价格
            order_amount += goodssku.pro_price * count

        # 计算订单的总金额
        try:
            order.order_money = order_amount
            order.save()
        except:
            return JsonResponse({"code": 8, "errmsg": "保存商品总金额失败!"})

        # 所有都成功, 删除购物车中的数据
        # r.hdel(cart_key, *sku_ids_int)

        # 成功后跳转确认支付页面
        return JsonResponse({"code": 0, "msg": "创建订单成功!", "order_sn": order_sn})


class OrderShow(BaseVerifyView):
    """确认支付页面(显示订单信息)"""

    def get(self, request):
        # 接收用户id
        tellphone = request.session.get("tellphone")
        user = Users.objects.get(user_telphone=tellphone)
        # 接收order_sn
        order_number = request.GET.get("order_sn")

        try:
            order = OderInfo.objects.get(order_number=order_number, user_id=user)
        except OderInfo.DoesNotExist:
            return redirect("cart:cart_info")

        # 计算订单总金额
        total = order.order_money + order.order_transport_price
        # 渲染订单到页面
        context = {
            "order": order,
            "total": total,
            "order_number": order_number
        }
        return render(request, 'shop/order.html', context)

    def post(self, request):
        pass


class OrderPay(View):
    def get(self, request):
        pass

    def post(self, request):
        # 接收用户id
        tellphone = request.session.get("tellphone")
        user = Users.objects.get(user_telphone=tellphone)
        # 接收order_sn
        order_number = request.POST.get("order_id")
        print(order_number)
        try:
            order = OderInfo.objects.get(order_number=order_number, user_id=user)
        except OderInfo.DoesNotExist:
            return JsonResponse({"res": 0, "errmsg": "参数错误"})
        total = order.order_money + order.order_transport_price
        alipay = AliPay(
            appid="2016092400584130",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=os.path.join(settings.BASE_DIR, "order\\app_private_key.pem"),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=os.path.join(settings.BASE_DIR, "order\\alipay_public_key.pem"),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True,  # 默认False
        )

        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_number,
            total_amount=str(total),
            subject="手机商城",
            return_url=None,
            notify_url=None
        )
        pay_url = "https://openapi.alipay.com/gateway.do?" + order_string
        return JsonResponse({"res": 3, "pay_url": pay_url})
