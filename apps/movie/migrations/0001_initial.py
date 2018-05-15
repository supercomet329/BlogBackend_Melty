# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-15 02:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_content', models.TextField(help_text='原始内容', verbose_name='原始内容')),
                ('formatted_content', models.TextField(help_text='处理后内容', verbose_name='处理后内容')),
                ('add_time', models.DateTimeField(auto_now_add=True, help_text='添加时间', null=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='修改时间', null=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '电影详情',
                'verbose_name_plural': '电影详情列表',
            },
        ),
        migrations.CreateModel(
            name='MovieInfo',
            fields=[
                ('postbaseinfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='material.PostBaseInfo')),
                ('directors', models.CharField(blank=True, help_text='导演', max_length=255, null=True, verbose_name='导演')),
                ('actors', models.CharField(blank=True, help_text='演员', max_length=255, null=True, verbose_name='演员')),
                ('region', models.CharField(blank=True, help_text='地区', max_length=20, null=True, verbose_name='地区')),
                ('language', models.CharField(blank=True, help_text='语言', max_length=20, null=True, verbose_name='语言')),
                ('length', models.IntegerField(blank=True, default=0, help_text='时长', null=True, verbose_name='时长')),
            ],
            options={
                'verbose_name': '电影',
                'verbose_name_plural': '电影列表',
            },
            bases=('material.postbaseinfo',),
        ),
        migrations.AddField(
            model_name='moviedetail',
            name='movie_info',
            field=models.ForeignKey(blank=True, help_text='内容', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='details', to='movie.MovieInfo', verbose_name='内容'),
        ),
    ]
