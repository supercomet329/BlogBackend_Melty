# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-06-16 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0002_auto_20180524_0951'),
    ]

    operations = [
        migrations.RenameField(
            model_name='materialpicture',
            old_name='abstract',
            new_name='en_desc',
        ),
        migrations.RenameField(
            model_name='materialpicture',
            old_name='subtitle',
            new_name='en_title',
        ),
        migrations.RenameField(
            model_name='postbaseinfo',
            old_name='abstract',
            new_name='en_desc',
        ),
        migrations.RenameField(
            model_name='postbaseinfo',
            old_name='subtitle',
            new_name='en_title',
        ),
        migrations.RemoveField(
            model_name='materialcategory',
            name='subname',
        ),
        migrations.RemoveField(
            model_name='materiallicense',
            name='subname',
        ),
        migrations.RemoveField(
            model_name='materialtag',
            name='subname',
        ),
        migrations.AddField(
            model_name='materialcategory',
            name='en_name',
            field=models.CharField(default='', help_text='英文名', max_length=30, verbose_name='英文名'),
        ),
        migrations.AddField(
            model_name='materiallicense',
            name='en_name',
            field=models.CharField(default='', help_text='英文名', max_length=30, verbose_name='英文名'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='materialtag',
            name='en_name',
            field=models.CharField(default='', help_text='英文名', max_length=30, verbose_name='英文名'),
            preserve_default=False,
        ),
    ]
