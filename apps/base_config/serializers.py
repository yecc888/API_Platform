__author__ = 'yecc'
__date__ = '2019/11/29 16:03'

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import EnvManager, ProjectManager, ModelManager


# serializers,如果有外键，通过嵌套，可以展示外键的值

class EnvSerializer(serializers.ModelSerializer):
    """
    环境管理序列化
    """
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = EnvManager
        # fields = ['env_name', 'env_desc', 'env_type', 'host', 'port', 'env_status', 'create_time', 'env_info']
        fields = "__all__"

    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     创建数据
    #     """
    #     return EnvManager.objects.create(**validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目管理序列化
    """
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    open_time = serializers.DateField(label='项目开始日期', required=True)
    close_time = serializers.DateField(label='项目结束日期', required=True)


    class Meta:
        model = ProjectManager
        fields = "__all__"


class ModelSerializer(serializers.ModelSerializer):
    """
    模块序列化

    """
    project = ProjectSerializer()
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = ModelManager
        fields = "__all__"
