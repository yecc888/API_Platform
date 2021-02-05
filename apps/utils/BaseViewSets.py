# Base类，将增删改查方法重写
# !/usr/bin/env python
# -*- coding:utf-8 -*-

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from apps.utils.response import CoustomResponse
from rest_framework import filters
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend

"""
get_queryset：获取QuerySet数据集合
get_object：获取单条数据对象
get_serializer：获取对应的model序列化器
get_serializer_class：获取序列化器对应的model实体类
get_serializer_context：提供给序列化程序类的额外上下文
filter_queryset：过滤QuerySet数据集合
paginator：分页器
paginate_queryset：对数据进行切片
get_paginated_response：获取分页返回的数据response
"""


class CustomViewBase(viewsets.ModelViewSet):
    # pagination_class = LargeResultsSetPagination
    # filter_class = ServerFilter
    queryset = ''
    serializer_class = ''
    permission_classes = ()
    filter_fields = ()
    search_fields = ()
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return CoustomResponse(data=serializer.data, msg="success", code=201, status=status.HTTP_201_CREATED,
                               headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return CoustomResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CoustomResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return CoustomResponse(data=serializer.data, msg="success", code=200, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return CoustomResponse(data=[], code=204, msg="delete resource success", status=status.HTTP_204_NO_CONTENT)
