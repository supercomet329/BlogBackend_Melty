# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-06-18 05:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0003_auto_20180617_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='postbaseinfo',
            name='index',
            field=models.IntegerField(default=0, help_text='置顶', verbose_name='置顶'),
        ),
    ]
