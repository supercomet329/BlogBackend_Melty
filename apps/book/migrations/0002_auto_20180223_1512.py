# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-23 07:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookdetail',
            name='book_info',
            field=models.ForeignKey(blank=True, help_text='内容', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='details', to='book.BookInfo', verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='booknotedetail',
            name='book_note_info',
            field=models.ForeignKey(blank=True, help_text='内容', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='details', to='book.BookNoteInfo', verbose_name='内容'),
        ),
    ]
