from django.db import models


# Create your models here.

class UserAddress(models.Model):
    """
    收获地址表
    ID
    用户ID
    收货人 姓名
    手机号码
    省ID
    市ID
    区ID
    街道ID
    详细描述
    是否是默认地址
    添加时间
    修改时间
    是否删除
    """
    user_id = models.ForeignKey(to="user_info.Users", verbose_name="用户ID")
    goods_user_name = models.CharField(max_length=32, verbose_name="用户ID")
    goods_user_phone = models.CharField(max_length=16, verbose_name="手机号码")
    goods_detail = models.CharField(max_length=50, verbose_name="详细描述", null=True, blank=True)
    default_address = models.BooleanField(default=False, verbose_name="是否是默认地址")
    province_id = models.IntegerField(verbose_name="省ID")
    city_id = models.IntegerField(verbose_name="市ID")
    district_id = models.IntegerField(verbose_name="区ID")
    street_id = models.IntegerField(verbose_name="街道ID")
    address_add_time = models.DateTimeField(auto_now_add=True, verbose_name="地址添加时间")
    address_edit_time = models.DateTimeField(auto_now=True, verbose_name="地址修改时间")
    address_status = models.BooleanField(default=False, verbose_name="地址删除状态")

    def __str__(self):
        return self.goods_detail

    class Meta:
        verbose_name = "收获地址管理"
        verbose_name_plural = verbose_name
