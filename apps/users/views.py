from django.contrib.auth import get_user_model
from .utils import get_user
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions, serializers
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from django.contrib.auth.backends import ModelBackend
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler


from .serializers import UersInfoSerializers, AddUserSerializers
from base_config.views import BasePagination

User = get_user_model()


class CoustomBackend(ModelBackend):
    """
    自定义用户验证,可以手机号、邮箱登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = get_user(username)
            if user.check_password(password):
                return user
        except Exception as e:
            raise serializers.ValidationError({'username_error_field': "用户名错误！", 'code': -1})
            return None
        else:
            raise serializers.ValidationError({'password_error_field': '密码错误！', 'code': -2})
            return None


class UserViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin,mixins.CreateModelMixin,
                  mixins.DestroyModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    用户管理
       list:
        获取用户列表
    create:
        创建用户
    delete:
        删除用户
    update:
        更新用户
    retrieve:
         某个用户信息
    """
    pagination_class = BasePagination
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = (IsAuthenticated,)
    search_fields = ['username', 'mobile']
    ordering_fields = ['create_time', 'username']
    ordering = ['-create_time']

    queryset = User.objects.all()
    serializer_class = AddUserSerializers





# class AddUserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
#
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
#     queryset = User.objects.all()
#     serializer_class = AddUserSerializers

    # def get_serializer_class(self):
    #     """
    #     动态获取序列化类
    #     :return:
    #     """
    #     if self.action == 'create':
    #         return AddUserSerializers
    #     elif self.action == "retrieve":
    #         return UersInfoSerializers
    #
    #     return UersInfoSerializers

    # def get_permissions(self):
    #     """
    #     动态添加权限
    #     :return:
    #     """
    #     if self.action == 'create':
    #         return []
    #     elif self.action == "retrieve":
    #         return [permissions.IsAuthenticated()]
    #
    #     return [permissions.IsAuthenticated()]

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = self.perform_create(serializer)
    #     re_dict = serializer.data
    #     payload = jwt_payload_handler(user)
    #     re_dict["token"] = jwt_encode_handler(payload)
    #     re_dict["name"] = user.name if user.name else user.username
    #
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def get_object(self):
    #     return self.request.user
    #
    # def perform_create(self, serializer):
    #     return serializer.save()
