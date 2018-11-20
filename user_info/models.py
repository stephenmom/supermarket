from django.db import models
from myrandom import random_user_info


class Users(models.Model):
    #  用户模型,用户的对象属性有
    #  用户名 ,密码 ,性别, 出生日期,
    #  学校 ,详细地址 ,手机号码
    GENDER_CHOICES = (
        (0, '男性'),
        (1, '女性'),
        (2, '保密'),
    )
    user_name = models.CharField(max_length=32, verbose_name='用户名', null=True)
    user_password = models.CharField(max_length=16)
    user_telphone = models.CharField(max_length=15, verbose_name='手机号码')
    user_gender = models.IntegerField(choices=GENDER_CHOICES, verbose_name='性别', default=2)
    user_brith = models.DateField(auto_now_add=True, verbose_name="出生日期", null=True)
    user_school = models.CharField(max_length=40, verbose_name="学校", null=True)
    user_address = models.CharField(max_length=40, verbose_name="详细地址", null=True)
    user_hometown = models.CharField(max_length=43, verbose_name="故乡", null=True)
