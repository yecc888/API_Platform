from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import logging
from collections import OrderedDict, namedtuple

from .filter import EnvsFilter, ProjectDynamicFilter, ProjectFilter, ModelFilter  # 过滤器
from .models import EnvManager, ProjectManager, ModelManager, ProjectDynamic
from .serializers import EnvSerializer, ProjectSerializer, \
    ModelSerializer, ProjectDynamicSerializer, ModelDeSerializer
from .utils import record_dynamic

logger = logging.getLogger(__name__)


class BasePagination(PageNumberPagination):
    # 分页逻辑
    page_size = 10  # 默认每页显示个数配置
    page_size_query_param = 'pageSize'  # 每页多少条数
    page_query_param = 'pageNum'  # 第几页
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))


class EnvsListViewSet(viewsets.ModelViewSet):
    """
    环境管理页，分页、搜索、过滤、排序
    采用viewsets写法
    """
    queryset = EnvManager.objects.all()
    serializer_class = EnvSerializer
    pagination_class = BasePagination
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_class = EnvsFilter
    search_fields = ['name', 'host']
    ordering_fields = ['id', 'create_time']
    ordering = ['-m_time']


class ProjectViewSet(viewsets.ModelViewSet):
    """"
    项目管理
    list:
        获取项目列表
    create:
        创建项目
    delete:
        删除项目
    update:
        更新项目
    """
    pagination_class = BasePagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = ProjectManager.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'sn']
    filter_class = ProjectFilter
    ordering_fields = ['create_time', 'name']
    ordering = ['-create_time']


class ModelViewSet(viewsets.ModelViewSet):
    """"
    模块管理
    list:
        获取模块列表
    create:
        创建模块
    delete:
        删除模块
    update:
        更新模块
    """
    pagination_class = BasePagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = ModelManager.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    filter_class = ModelFilter
    ordering_fields = ['create_time', 'name']
    ordering = ['-create_time']

    def get_serializer_class(self):
        if self.action == "list":
            return ModelDeSerializer
        elif self.action == "create":
            return ModelSerializer
        elif self.action == 'update':
            return ModelSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        datas = self.do_req_data(request.data)
        serializer = self.get_serializer(instance, data=datas, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def do_req_data(self, datas):
        for k, v in datas.items():
            # if isinstance(v, list):
            #     dlist = []
            #     for i, j in enumerate(v):
            #         dlist.append(j['id'])
            #     datas.update({k: dlist})
            if isinstance(v, dict):
                datas.update({k: v['id']})
        datas.pop("m_time")
        datas.pop("create_time")
        return datas


class ProjectDynamicViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    """
    获取项目动态信息
    """
    serializer_class = ProjectDynamicSerializer
    # 分页
    pagination_class = BasePagination
    # 权限
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # 验证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # 搜索 =types精确搜索
    search_fields = ['=types', "operationObject", "description"]
    # 排序
    ordering_fields = ['time', 'types']
    ordering = ['-time']
    # 过滤
    # filter_fields = ['types','description']
    filter_class = ProjectDynamicFilter  # 自定义过滤器

    # lookup_field = "project_id"

    def get_queryset(self):
        if self.action == "list":
            return ProjectDynamic.objects.all()
