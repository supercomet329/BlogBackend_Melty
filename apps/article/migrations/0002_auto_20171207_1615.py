# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-07 08:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articletag',
            options={'verbose_name': '文章标签', 'verbose_name_plural': '文章标签'},
        ),
        migrations.AlterField(
            model_name='articleinfo',
            name='front_image_type',
            field=models.CharField(choices=[('0', '无'), ('1', '小图'), ('2', '大图')], default='无', help_text='封面图类别', max_length=20, verbose_name='封面图类别'),
        ),
    ]
