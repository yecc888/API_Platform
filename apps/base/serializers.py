__author__ = 'yecc'
__date__ = '2019/11/29 16:03'

from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import EnvManager, ProjectManager, ModelManager, ProjectDynamic
from users.serializers import AddUserSerializers, UersInfoSerializers, UerModelSerializers
from apps.utils.get_id import getId_byName

# serializers,如果有外键，通过嵌套，可以展示外键的值

user = get_user_model()


class EnvSerializer(serializers.ModelSerializer):
    """
    环境管理序列化
    """
    name = serializers.CharField(required=True, max_length=10, allow_blank=False, label="环境名称",
                                 error_messages={"blank": "名称不能为空",
                                                 "required": "名称必输"}
                                 )
    host = serializers.CharField(required=True, max_length=126, allow_blank=False, label="IP/域名",
                                 error_messages={"blank": "IP/域名不能为空",
                                                 "required": "IP/域名必输"}
                                 )
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    m_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = EnvManager
        # fields = ['name', 'desc', 'type', 'host', 'port', 'status']
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目管理序列化
    """
    name = serializers.CharField(required=True, allow_blank=False, label="项目名称", max_length=20,
                                 error_messages={"blank": "请输入项目名称",
                                                 "required": "请输入项目名称",
                                                 "max_length": "字数大于20个字符，请重新输入"},
                                 validators=[UniqueValidator(queryset=ProjectManager.objects.all(),
                                                             message="项目已经存在，请重新输入")])
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    m_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    open_time = serializers.DateField(label='项目开始日期', required=True,
                                      error_messages={"required": "请输入项目开始日期"})
    close_time = serializers.DateField(label='项目结束日期', required=True,
                                       error_messages={"required": "请输入项目结束日期"})

    class Meta:
        model = ProjectManager
        fields = "__all__"


class ProjectModelSerializer(serializers.ModelSerializer):
    """
    模块对应项目序列化
    """
    # name = serializers.CharField(required=True, allow_blank=False, error_messages={"blank": "请输入项目名称",
    #                                                                                "required": "请输入项目名称"
    #                                                                                })
    #
    # def validate_name(self, name):
    #     # ss = ProjectManager.objects.filter(name=self.initial_data["username"])
    #     exsit = ProjectManager.objects.filter(name=name)
    #     if len(exsit) == 0:
    #         raise serializers.ValidationError("项目不存在，请重新输入")
    #     return name

    class Meta:
        model = ProjectManager
        fields = ("id", "name")


class ModelSerializer(serializers.ModelSerializer):
    """
    模块序列化

    """
    name = serializers.CharField(required=True, max_length=100, allow_blank=False, label="模块名称",
                                 error_messages={"blank": "名称不能为空",
                                                 "required": "名称必输"}
                                 )
    # model_owner = UerModelSerializers(many=True)
    # project = ProjectModelSerializer(many=False)
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    m_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = ModelManager
        fields = "__all__"


class pModelSerializer(serializers.ModelSerializer):
    """
    父模块序列化
    """
    class Meta:
        model = ModelManager
        fields = ("id", "name")


class ModelDeSerializer(serializers.ModelSerializer):
    """
    模块序反列化

    """
    name = serializers.CharField(required=True, max_length=100, allow_blank=False, label="模块名称",
                                 error_messages={"blank": "名称不能为空",
                                                 "required": "名称必输"}
                                 )
    model_owner = UerModelSerializers(many=True)
    project = ProjectModelSerializer(many=False)
    parent_model = pModelSerializer()
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    m_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = ModelManager
        fields = "__all__"


class ModelInterfaceSerializer(serializers.ModelSerializer):
    """
    接口对应模块序列化
    """

    name = serializers.CharField(required=True, allow_blank=False, error_messages={"blank": "请输入模块名称",
                                                                                   "required": "请输入模块名称"
                                                                                   })

    def validate_name(self, name):
        exsit = ModelManager.objects.filter(name=name)
        if len(exsit) == 0:
            raise serializers.ValidationError("模块不存在，请重新输入")
        return name

    class Meta:
        model = ModelManager
        fields = ["id", "name"]


class EnvInterfaceSerializer(serializers.ModelSerializer):
    """
    接口对应环境序列化
    """
    name = serializers.CharField(required=True, allow_blank=False, error_messages={"blank": "请输入环境名称",
                                                                                   "required": "请输入环境名称"
                                                                                   })

    def validate_name(self, name):
        exsit = EnvManager.objects.filter(name=name)
        if len(exsit) == 0:
            raise serializers.ValidationError("环境不存在，请重新输入")
        return name

    class Meta:
        model = EnvManager
        fields = ["id", "name"]


class ProjectDynamicSerializer(serializers.ModelSerializer):
    """
    项目动态序列化
    """
    time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    user = UerModelSerializers()

    class Meta:
        model = ProjectDynamic
        fields = ["id","types", "operationObject", "description", "user", "time"]


class ProjectDynamicDeserializer(serializers.ModelSerializer):
    """
    项目动态序反列化
    """
    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault())
    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = ProjectDynamic
        fields = ["types", "operationObject",
                  "description", "time", "user"]

