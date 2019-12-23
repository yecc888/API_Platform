from django.shortcuts import render

# Create your views here.
from .models import EnvManager, ProjectManager
from .serializers import EnvSerializer, ProjectSerializer
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filter import EnvsFilter  # 过滤器


class BasePagination(PageNumberPagination):
    # 分页逻辑
    page_size = 10
    page_size_query_param = 'pageSize'  # 每页多少条数
    page_query_param = 'pageNum'  # 第几页
    max_page_size = 100


class EnvsListViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
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
    search_fields = ['env_name', 'host']
    ordering_fields = ['id', 'create_time']
    ordering = ['create_time']


    # filterset_fields = ['env_name', 'env_status']

    # def get_queryset(self):
    #     """
    #     过滤数据，可以自己定义
    #     :return:
    #     """

class ProjectViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                     mixins.ListModelMixin, mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin, viewsets.GenericViewSet):
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
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = ProjectManager.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['project_name']
    ordering_fields = ['create_time', 'project_name']
    ordering = ['-create_time']
