# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-19 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(default='ZDYyBShF7', max_length=32, verbose_name='用户名')),
                ('user_password', models.CharField(max_length=16)),
                ('user_telphone', models.CharField(max_length=15, verbose_name='手机号码')),
                ('user_gender', models.IntegerField(choices=[(0, '男性'), (1, '女性'), (2, '保密')], default=2, verbose_name='性别')),
                ('user_brith', models.DateField(auto_now_add=True, verbose_name='出生日期')),
                ('user_school', models.CharField(max_length=40, verbose_name='学校')),
                ('user_address', models.CharField(max_length=40, verbose_name='详细地址')),
                ('user_hometown', models.CharField(max_length=43, verbose_name='故乡')),
            ],
        ),
    ]
