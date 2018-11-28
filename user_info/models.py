from django.db import models


class Users(models.Model):
    #  用户模型,用户的对象属性有
    #  用户名 ,密码 ,性别, 出生日期,
    #  学校 ,详细地址 ,手机号码
    GENDER_CHOICES = (
        (1, '男性'),
        (2, '女性'),
    )
    user_head = models.ImageField(upload_to='user', verbose_name='头像', default='user/10.jpg', max_length=500)
    user_name = models.CharField(max_length=32, verbose_name='用户名', null=True)
    user_password = models.CharField(max_length=16)
    user_telphone = models.CharField(max_length=15, verbose_name='手机号码')
    user_gender = models.IntegerField(choices=GENDER_CHOICES, verbose_name='性别', default=1)
    user_brith = models.DateField(auto_now_add=True, verbose_name="出生日期", null=True)
    user_school = models.CharField(max_length=40, verbose_name="学校", null=True, blank=True)
    user_address = models.CharField(max_length=40, verbose_name="详细地址", null=True, blank=True)
    user_hometown = models.CharField(max_length=43, verbose_name="故乡", null=True, blank=True)
    is_delete = models.BooleanField(default=False, verbose_name="删除状态")

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name


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
    user_id = models.ForeignKey(to="Users", verbose_name="创建人")
    goods_user_name = models.CharField(max_length=32, verbose_name="收货人")
    goods_user_phone = models.CharField(max_length=16, verbose_name="收货人电话")
    goods_detail = models.CharField(max_length=50, verbose_name="详细地址", null=True, blank=True)
    default_address = models.BooleanField(default=False, verbose_name="是否设置为默认地址")
    province_id = models.CharField(max_length=16, verbose_name="省名字")
    city_id = models.CharField(max_length=16, verbose_name="市名字")
    district_id = models.CharField(max_length=16, verbose_name="区名字")
    street_id = models.IntegerField(verbose_name="街道名字", null=True, blank=True)
    address_add_time = models.DateTimeField(auto_now_add=True, verbose_name="地址添加时间")
    address_edit_time = models.DateTimeField(auto_now=True, verbose_name="地址修改时间")
    address_status = models.BooleanField(default=False, verbose_name="地址删除状态")

    def __str__(self):
        return self.goods_detail

    class Meta:
        verbose_name = "收获地址管理"
        verbose_name_plural = verbose_name
