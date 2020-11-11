__author__ = 'yecc'
__date__ = '2019/12/20 11:27'

from rest_framework import routers, serializers
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from rest_framework.serializers import raise_errors_on_nested_writes
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from .models import sidebarInfo,useInfo


from rest_framework.utils import model_meta
import re
User = get_user_model()


class UersInfoSerializers(serializers.ModelSerializer):
    """
    用户信息序列化
    """

    class Meta:
        model = User
        fields = ('name', 'mobile', 'user_roles', 'email', 'id')


class UerModelSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'id')


class AddUserSerializers(serializers.ModelSerializer):
    """
    增加用户序列化
    """
    username = serializers.CharField(label='用户名', help_text='用户名', required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'},
                                     help_text="密码", label="密码", write_only=True,required=False)
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    mobile = serializers.CharField(label='手机号', help_text='手机号',
                                   validators=[UniqueValidator(queryset=User.objects.all(),
                                                               message='手机号已存在')])

    def validate(self, attrs):
        # 验证密码，部分更新时，可以不输入密码，既可以不更改密码
        # 创建时必须输入密码
        passwords = attrs.get("password")
        if passwords:
            pass
        return attrs

    def create(self, validated_data):
        user = super(AddUserSerializers, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.mobile = validated_data['mobile']
        instance.email = validated_data['email']
        instance.user_roles = validated_data['user_roles']
        user = super(AddUserSerializers, self).update(instance, validated_data)
        # 处理密码修改
        try:
            if validated_data.get('password'):
                   pw = make_password(validated_data["password"])
                   user.password = pw
                   user.save()
        except Exception as ex:
            raise

        instance.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'mobile', 'email', 'user_roles', 'create_time', 'id')


class sidebarInfoSerializer(serializers.ModelSerializer):
    """
    侧边栏序列化
    """
    class Meta:
        model = sidebarInfo
        fields = '__all__'


class InfoSerializer(serializers.ModelSerializer):
    """
    导航序列化
    """
    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault())
    user = UerModelSerializers()
    menus = sidebarInfoSerializer(many=True)
    icon = serializers.ImageField()

    class Meta:
        model = useInfo
        fields = ["id", "icon", "menus", "user"]
