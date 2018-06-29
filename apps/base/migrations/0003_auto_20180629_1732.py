# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-06-29 09:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20180617_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='force_refresh_time',
            field=models.DateTimeField(blank=True, help_text='该时间会返回给前端，前端通过将浏览器本地存储的时间与这个时间进行比对，如果浏览器本地存储的强制刷新时间比这个时间早，就会执行强制刷新浏览器本地缓存', null=True, verbose_name='强制刷新时间'),
        ),
        migrations.AlterField(
            model_name='siteinfo',
            name='is_force_refresh',
            field=models.BooleanField(default=False, help_text='用于控制前端页面是否强制刷新本地缓存', verbose_name='是否强制刷新'),
        ),
    ]
