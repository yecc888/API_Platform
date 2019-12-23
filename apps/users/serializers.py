__author__ = 'yecc'
__date__ = '2019/12/20 11:27'

from rest_framework import routers, serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UersInfoSerializers(serializers.ModelSerializer):
    """
    用户信息序列化
    """

    class Meta:
        model = User
        fields = ('name', 'mobile', 'user_roles', 'email', 'id')


class AddUserSerializers(serializers.ModelSerializer):
    """
    增加用户序列化
    """
    username = serializers.CharField(label='用户名', help_text='用户名', required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message='用户名已存在')])
    password = serializers.CharField(style={'input_type': 'password'},
                                     help_text="密码", label="密码", write_only=True)
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    mobile = serializers.CharField(label='手机号', help_text='手机号',
                                   validators=[UniqueValidator(queryset=User.objects.all(),
                                                               message='手机号已存在')])

    def create(self, validated_data):
        user = super(AddUserSerializers, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'mobile', 'email', 'user_roles', 'create_time', 'id')
