__author__ = 'yecc'
__date__ = '2020/5/4 16:23'

import django_filters

from .models import ApiManagerment,Headers, CustomParameters, ApiMock
from base.models import ModelManager


class ApiFilter(django_filters.rest_framework.FilterSet):
    """
    环境名称过滤
    contains：模糊过滤，icontains:忽略大小写
    """
    model__name = django_filters.CharFilter(method='filter_model')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # 自定义过滤外键字段
    def filter_model(self, queryset, name, value):
        q = ModelManager.objects.filter(name=value)
        return queryset.filter(model_id=q)

    class Meta:
        model = ApiManagerment
        fields = ['name', 'model__name']


class HeaderTempFilter(django_filters.rest_framework.FilterSet):
    """
    环境名称过滤
    contains：模糊过滤，icontains:忽略大小写
    """
    value = django_filters.CharFilter(field_name='value', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Headers
        fields = ['value', 'name']


class CustomParaFilter(django_filters.rest_framework.FilterSet):
    """
    参数名称过滤
    """
    key = django_filters.CharFilter(field_name='key', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = CustomParameters
        fields = ['key', 'name']


class ApiMockFilter(django_filters.rest_framework.FilterSet):
    """
    mock接口参数过滤
    """
    url = django_filters.CharFilter(field_name='url', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    status = django_filters.NumberFilter(field_name='status', lookup_expr='icontains')

    class Meta:
        model = ApiMock
        fields = ['url', 'name', 'status']
