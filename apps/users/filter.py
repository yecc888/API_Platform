__author__ = 'yecc'
__date__ = '2020/4/28 14:26'

import django_filters
from django.contrib.auth import get_user_model

User = get_user_model()


class userFilter(django_filters.rest_framework.FilterSet):
    """
    环境名称过滤
    contains：模糊过滤，icontains:忽略大小写
    """
    mobile = django_filters.CharFilter(field_name='mobile', lookup_expr='contains', help_text='手机号')
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username', 'mobile']
