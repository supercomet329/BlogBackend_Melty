# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-22 07:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloggerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='名称', max_length=20, verbose_name='名称')),
                ('name_en', models.CharField(default='', help_text='名称英文', max_length=20, verbose_name='名称英文')),
                ('desc', models.CharField(default='', help_text='简介', max_length=300, verbose_name='简介')),
                ('avatar', models.ImageField(blank=True, help_text='头像', null=True, upload_to='base/avatar/image/%y/%m', verbose_name='头像')),
                ('background', models.ImageField(blank=True, help_text='背景图', null=True, upload_to='base/image/background/%y/%m', verbose_name='背景图')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '个人信息',
                'verbose_name_plural': '个人信息',
            },
        ),
        migrations.CreateModel(
            name='BloggerMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='名称', max_length=20, verbose_name='名称')),
                ('index', models.IntegerField(default=0, help_text='顺序', verbose_name='顺序')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间')),
                ('blogger', models.ForeignKey(help_text='个人', on_delete=django.db.models.deletion.CASCADE, to='base.BloggerInfo', verbose_name='个人')),
                ('master', models.ForeignKey(help_text='技能', on_delete=django.db.models.deletion.CASCADE, to='material.MaterialMaster', verbose_name='技能')),
            ],
            options={
                'verbose_name': '技能信息',
                'verbose_name_plural': '技能信息',
            },
        ),
        migrations.CreateModel(
            name='BloggerSocial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='名称', max_length=20, verbose_name='名称')),
                ('index', models.IntegerField(default=0, help_text='顺序', verbose_name='顺序')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间')),
                ('blogger', models.ForeignKey(help_text='个人', on_delete=django.db.models.deletion.CASCADE, to='base.BloggerInfo', verbose_name='个人')),
                ('social', models.ForeignKey(help_text='社交平台', on_delete=django.db.models.deletion.CASCADE, to='material.MaterialSocial', verbose_name='社交平台')),
            ],
            options={
                'verbose_name': '社交信息',
                'verbose_name_plural': '社交信息',
            },
        ),
        migrations.CreateModel(
            name='FriendLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='名称', max_length=30, verbose_name='名称')),
                ('desc', models.CharField(help_text='简介', max_length=100, verbose_name='简介')),
                ('image', models.ImageField(blank=True, help_text='图片', null=True, upload_to='base/friendlink/image/%y/%m', verbose_name='图片')),
                ('url', models.URLField(help_text='链接', verbose_name='链接')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '友情链接',
                'verbose_name_plural': '友情链接',
            },
        ),
        migrations.CreateModel(
            name='SiteInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', help_text='名称', max_length=20, verbose_name='名称')),
                ('name_en', models.CharField(default='', help_text='名称英文', max_length=20, verbose_name='名称英文')),
                ('desc', models.CharField(default='', help_text='简介', max_length=20, verbose_name='简介')),
                ('icon', models.ImageField(blank=True, help_text='图标', null=True, upload_to='base/site/image/%y/%m', verbose_name='图标')),
                ('copyright', models.CharField(default='', help_text='版权', max_length=100, verbose_name='版权')),
                ('icp', models.CharField(default='', help_text='ICP', max_length=20, verbose_name='ICP')),
                ('is_live', models.BooleanField(default=False, help_text='是否激活', verbose_name='是否激活')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '网站信息',
                'verbose_name_plural': '网站信息',
            },
        ),
        migrations.AddField(
            model_name='bloggerinfo',
            name='masters',
            field=models.ManyToManyField(through='base.BloggerMaster', to='material.MaterialMaster'),
        ),
        migrations.AddField(
            model_name='bloggerinfo',
            name='socials',
            field=models.ManyToManyField(through='base.BloggerSocial', to='material.MaterialSocial'),
        ),
    ]
