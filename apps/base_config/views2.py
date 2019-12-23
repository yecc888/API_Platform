from django.shortcuts import render

# Create your views here.
from .models import EnvManager
from .serializers import EnvSerializer
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination


class EnvsPagination(PageNumberPagination):
    # 分页逻辑
    page_size = 5
    page_size_query_param = 'pageSize'  # 每页多少条数
    page_query_param = 'pageNum'  # 第几页
    max_page_size = 100


class EnvsListView(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                   generics.GenericAPIView):
    """
    环境管理页
    采用mixins，GenericAPIView写法,带有自动分页等功能
    """
    queryset = EnvManager.objects.all()
    serializer_class = EnvSerializer
    pagination_class = EnvsPagination

    # 必须重写get方法
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # 必须重写post方法
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
