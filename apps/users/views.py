from django.contrib.auth import get_user_model
from .utils import get_user
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions, serializers
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from django.contrib.auth.backends import ModelBackend
from rest_framework import permissions
from datetime import datetime
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from threading import local
from uuid import uuid4
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_jwt.views import JSONWebTokenAPIView,jwt_response_payload_handler
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework.response import Response
from .filter import userFilter
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler


from .serializers import UersInfoSerializers, AddUserSerializers, sidebarInfoSerializer, InfoSerializer
from base.views import BasePagination
from .models import useInfo,sidebarInfo

User = get_user_model()

thread = local()


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


class ObtainJSONWebToken1(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            global thread, us1
            us1 = user.username
            thread.user = user.username
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_users(self):
    print(thread.user)
    print(us1)

    return thread.user


obtain_jwt_token1 = ObtainJSONWebToken1.as_view()


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
    # permission_classes = (IsAuthenticated,)
    search_fields = ['username', 'mobile']
    ordering_fields = ['create_time', 'username']
    ordering = ['-create_time']
    filter_class = userFilter
    queryset = User.objects.all()
    serializer_class = AddUserSerializers

    def get_permissions(self):
        if self.action != 'list':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        else:
            return [permissions.IsAuthenticated()]


# class UserInfo(mixins.ListModelMixin,GenericViewSet):
class UserInfoView(APIView):
    """
    用户导航列表
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        获取用户导航栏信息
        :param request:
        :return:
        """
        role = []
        r = useInfo.objects.values('role')
        role.append(str(r[0]['role']))
        obj = useInfo.objects.all()
        obj_serializers = InfoSerializer(obj, many=True)

        return Response(data={"role": role, "data": obj_serializers.data})


class UserInfoView1(mixins.ListModelMixin, GenericViewSet):
    """
    获取用户信息，动态展示前端侧边栏导航
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = InfoSerializer
    queryset = useInfo.objects.all().order_by('user__id')
    pagination_class = BasePagination
    ordering = ['-id']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        role = []
        r = useInfo.objects.values('role')
        role.append(str(r[0]['role']))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(data={"role": role, "data": serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response(data={"role": role, "data": serializer.data})


class Logout(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        """
        退出登录，修改JTW密钥
        :param request:
        :return:
        """
        # user = request.user
        # user.user_secret = uuid4()
        # user.save()
        return Response(data={"success"})




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
