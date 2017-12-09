#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2017/12/7 下午2:13
# @Author  : LennonChin
# @Email   : i@coderap.com
# @File    : apiview.py
# @Software: PyCharm

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins, viewsets, filters

from .models import MaterialCategory, Banner
from .serializers import CategorySerializer, SingleLevelCategorySerializer, BannerSerializer
from .filters import CategoryFilter


class CategoryListViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List:
        分类列表页
    """
    queryset = MaterialCategory.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CategoryFilter
    search_fields = ('name', 'code', 'desc')
    ordering_fields = ('category_type', 'is_tab')


class SingleLevelCategoryListViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List:
        单级分类列表页
    """
    queryset = MaterialCategory.objects.all()
    serializer_class = SingleLevelCategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CategoryFilter
    search_fields = ('name', 'code', 'desc')
    ordering_fields = ('category_type', 'is_tab')


class BannerListViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List:
        Banner列表页
    """
    queryset = Banner.objects.all().order_by("-index")
    serializer_class = BannerSerializer

