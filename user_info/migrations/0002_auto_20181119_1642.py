# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-19 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_address',
            field=models.CharField(max_length=40, null=True, verbose_name='详细地址'),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_brith',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='出生日期'),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_hometown',
            field=models.CharField(max_length=43, null=True, verbose_name='故乡'),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_name',
            field=models.CharField(default='PtV2ST', max_length=32, verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_school',
            field=models.CharField(max_length=40, null=True, verbose_name='学校'),
        ),
    ]
