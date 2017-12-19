# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-08 06:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0002_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='名称', max_length=30, verbose_name='名称')),
                ('desc', models.CharField(help_text='简介', max_length=100, verbose_name='简介')),
                ('images', models.ImageField(help_text='图片', upload_to='banner/%y/%m', verbose_name='图片')),
                ('url', models.URLField(help_text='链接', verbose_name='链接')),
                ('experience', models.FloatField(default=0, help_text='熟练度', verbose_name='熟练度')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '技能',
                'verbose_name_plural': '技能',
            },
        ),
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='名称', max_length=30, verbose_name='名称')),
                ('desc', models.CharField(help_text='简介', max_length=100, verbose_name='简介')),
                ('images', models.ImageField(help_text='图片', upload_to='banner/%y/%m', verbose_name='图片')),
                ('url', models.URLField(help_text='链接', verbose_name='链接')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '社交平台',
                'verbose_name_plural': '社交平台',
            },
        ),
        migrations.AlterField(
            model_name='banner',
            name='index',
            field=models.IntegerField(default=0, help_text='顺序', verbose_name='顺序'),
        ),
    ]
