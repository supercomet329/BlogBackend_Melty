# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-23 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloggerinfo',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, help_text='添加时间', null=True, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='bloggermaster',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, help_text='添加时间', null=True, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='bloggersocial',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, help_text='添加时间', null=True, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='friendlink',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, help_text='添加时间', null=True, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='navigationlink',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, help_text='添加时间', null=True, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='siteinfo',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, help_text='添加时间', null=True, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='siteinfonavigation',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, help_text='添加时间', null=True, verbose_name='添加时间'),
        ),
    ]
