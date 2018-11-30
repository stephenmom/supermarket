from django.db import models


# Create your models here.


class Payment(models.Model):
    """
        支付方式
    """
    pay_name = models.CharField(verbose_name='支付方式',
                                max_length=20
                                )
    payment_add_time = models.DateTimeField(auto_now_add=True, verbose_name="支付方式添加时间")
    payment_edit_time = models.DateTimeField(auto_now=True, verbose_name="支付方式修改时间")
    payment_status = models.BooleanField(default=False, verbose_name="支付方式删除状态")

    class Meta:
        verbose_name = "支付方式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pay_name


class Transport(models.Model):
    """
        名称
        价格
    """
    name = models.CharField(verbose_name='配送方式',
                            max_length=20
                            )
    money = models.DecimalField(verbose_name='金额',
                                max_digits=9,
                                decimal_places=2,
                                default=0
                                )
    transport_add_time = models.DateTimeField(auto_now_add=True, verbose_name="配送方式添加时间")
    transport_edit_time = models.DateTimeField(auto_now=True, verbose_name="配送方式修改时间")
    transport_status = models.BooleanField(default=False, verbose_name="配送方式删除状态")

    class Meta:
        verbose_name = "配送方式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class OderInfo(models.Model):
    """
        订单信息表
        ID
        订单编号
        订单金额
        用户ID
        收货人姓名
        收货人电话
        订单地址
        订单状态
        运输方式
        付款方式
        实付金额
        添加时间
        修改时间
        是否删除
    """
    ORDER_STATUS = (
        (0, "待付款"),
        (1, "待发货"),
        (2, "已发货"),
        (3, "完成"),
        (4, "已评价"),
        (5, "申请退款"),
        (6, "已退款"),
        (7, "取消订单")
    )
    order_number = models.CharField(max_length=64, verbose_name="订单编号", unique=True)
    order_money = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="订单总价格", default=0)
    user_id = models.ForeignKey(to="user_info.Users", verbose_name="用户id")
    order_user_name = models.CharField(max_length=32, verbose_name="收货人")
    order_user_phone = models.CharField(max_length=16, verbose_name="收货人电话")
    order_address = models.CharField(max_length=50, verbose_name="订单地址")
    order_status_now = models.IntegerField(choices=ORDER_STATUS, verbose_name='订单状态', default=0)
    order_transport = models.CharField(max_length=50, verbose_name="运输方式", null=True, blank=True)
    order_transport_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="运输价格")
    order_payment = models.ForeignKey(to="Payment", verbose_name="付款方式", null=True, blank=True)
    really_pay_money = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="实付金额", default=0)
    ORDER_add_time = models.DateTimeField(auto_now_add=True, verbose_name="订单信息添加时间")
    ORDER_edit_time = models.DateTimeField(auto_now=True, verbose_name="订单信息修改时间")
    ORDER_status = models.BooleanField(default=False, verbose_name="订单信息删除状态")

    class Meta:
        verbose_name = "订单信息管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_number


class OrderGoods(models.Model):
    """
        订单商品表
        订单ID
        商品SKU ID
        商品数量
        商品价格
    """
    order = models.ForeignKey(to="OderInfo", verbose_name="订单ID")
    goods_sku = models.ForeignKey(to="product.ProSKU", verbose_name="订单商品的SKUID")
    count = models.IntegerField(verbose_name="订单商品的数量")
    price = models.DecimalField(verbose_name="订单商品的价格", max_digits=9, decimal_places=2)

    def __str__(self):
        return self.order.order_number

    class Meta:
        db_table = "order_goods"
        verbose_name = "订单商品管理"
        verbose_name_plural = verbose_name
