#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 下午5:28
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : adminx.py
# @Software: PyCharm

import xadmin

import markdown
from django import forms

from .models import BookInfo, BookDetail, BookResource, BookNoteInfo, BookNoteDetail
from material.models import PostTag
from pagedown.widgets import AdminPagedownWidget


# 图书基本信息的model form
class BookDetailForm(forms.ModelForm):
    origin_content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = BookDetail
        fields = '__all__'


class BookDetailAdmin(object):
    form = BookDetailForm
    exclude = ['formatted_content']
    model = BookDetail
    extra = 1

    def save_models(self):
        # 转换Markdown为格式化的HTML
        self.new_obj.formatted_content = markdown.markdown(self.new_obj.origin_content,
                                                           extensions=[
                                                               'markdown.extensions.extra',
                                                               'markdown.extensions.codehilite',
                                                               'markdown.extensions.toc',
                                                           ])
        self.new_obj.save()


# 图书基本信息
class BookInfoAdmin(object):
    list_display = ['title', "category", "tags", "front_image", "front_image_type"]
    search_fields = ['title']
    exclude = ['post_type', 'browse_password_encrypt']

    class ArticleTagInline(object):
        model = PostTag
        extra = 1

    inlines = [ArticleTagInline, BookDetailAdmin]


# 章节信息的model form
class BookNoteDetailForm(forms.ModelForm):
    origin_content = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = BookNoteDetail
        fields = '__all__'


class BookNoteDetailAdmin(object):
    form = BookDetailForm
    exclude = ['formatted_content']
    model = BookNoteDetail
    extra = 1

    def save_models(self):
        # 转换Markdown为格式化的HTML
        self.new_obj.formatted_content = markdown.markdown(self.new_obj.origin_content,
                                                           extensions=[
                                                               'markdown.extensions.extra',
                                                               'markdown.extensions.codehilite',
                                                               'markdown.extensions.toc',
                                                           ])
        self.new_obj.save()


# 章节基本信息
class BookNoteInfoAdmin(object):
    list_display = ['title', 'book', "category", "tags", 'is_reading', 'is_completed', 'is_noted', "front_image", "front_image_type"]
    list_editable = ['is_reading', 'is_completed', 'is_noted']
    search_fields = ['title']
    exclude = ['post_type', 'browse_password_encrypt']

    class ArticleTagInline(object):
        model = PostTag
        extra = 1

    inlines = [ArticleTagInline, BookNoteDetailAdmin]


# 资源信息
class BookResourceAdmin(object):
    list_display = ['book', 'name', "download", "add_time"]
    search_fields = ['name']


xadmin.site.register(BookInfo, BookInfoAdmin)
xadmin.site.register(BookNoteInfo, BookNoteInfoAdmin)
xadmin.site.register(BookResource, BookResourceAdmin)
