__author__ = 'yecc'
__date__ = '2019/11/30 14:03'

import django_filters
from django.db.models import Q
from .models import EnvManager


class EnvsFilter(django_filters.rest_framework.FilterSet):
    """
    环境名称过滤
    contains：模糊过滤，icontains:忽略大小写
    """
    host = django_filters.CharFilter(field_name='host', lookup_expr='contains', help_text='ip/域名')
    name = django_filters.CharFilter(field_name='env_name', lookup_expr='icontains')

    class Meta:
        model = EnvManager
        fields = ['name', 'env_status', 'host']

