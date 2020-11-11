__author__ = 'yecc'
__date__ = '2019/11/30 14:03'

import django_filters
from django.db.models import Q
from .models import EnvManager, ProjectDynamic, ProjectManager, ModelManager


class EnvsFilter(django_filters.rest_framework.FilterSet):
    """
    环境名称过滤
    contains：模糊过滤，icontains:忽略大小写
    """
    host = django_filters.CharFilter(field_name='host', lookup_expr='contains', help_text='ip/域名')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = EnvManager
        fields = ['name', 'status', 'host']


class ProjectDynamicFilter(django_filters.rest_framework.FilterSet):
    """
    项目动态过滤
    contains：模糊过滤，icontains:忽略大小写
    """
    types = django_filters.CharFilter(field_name='types', lookup_expr='contains', help_text='操作类型')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains',
                                            help_text="描述")
    operationObject = django_filters.CharFilter(field_name='operationObject', lookup_expr='icontains',
                                                help_text="操作对象")

    class Meta:
        model = ProjectDynamic
        fields = ['types', 'description', 'operationObject']


class ProjectFilter(django_filters.rest_framework.FilterSet):
    """
    项目信息过滤
    contains：模糊过滤，icontains:忽略大小写
    """
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains',
                                     help_text='项目名称')
    sn = django_filters.CharFilter(field_name='sn', lookup_expr='icontains',
                                   help_text="项目编号")

    class Meta:
        model = ProjectManager
        fields = ['name', 'sn']


class ModelFilter(django_filters.rest_framework.FilterSet):
    """
    项目信息过滤
    contains：模糊过滤，icontains:忽略大小写
    """
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains',
                                     help_text='模块名称')
    model_owner = django_filters.CharFilter(field_name='model_owner', lookup_expr='icontains',
                                            help_text="模块负责人")

    class Meta:
        model = ModelManager
        fields = ['name', 'model_owner']
