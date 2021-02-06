__author__ = 'yecc'
__date__ = '2020/5/4 16:23'

import django_filters

from .models import ApiManagerment,Headers, CustomParameters, ApiMock,CaseManagerment,CaseGroup
from base.models import ModelManager


class ApiFilter(django_filters.rest_framework.FilterSet):
    """
    接口过滤
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
    请求头模板过滤
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


class CaseFilter(django_filters.rest_framework.FilterSet):
    """
    mock接口参数过滤
    """
    caseType = django_filters.CharFilter(field_name='caseType', lookup_expr='icontains')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    caseStatus = django_filters.NumberFilter(field_name='caseStatus', lookup_expr='icontains')
    caseLevel = django_filters.NumberFilter(field_name='caseLevel', lookup_expr='icontains')
    case_group = django_filters.NumberFilter(field_name='case_group')

    def filter_case_group(self, queryset, name, value):
        q = CaseGroup.objects.filter(id=value)
        return queryset.filter(case_group_id=q)

    class Meta:
        model = CaseManagerment
        fields = ['name', 'caseStatus','caseType','caseLevel','case_group']