from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField
from django.contrib.auth import get_user_model
user = get_user_model()
# Create your models here.


class ProjectManager(models.Model):
    """
    项目管理
    """
    id = models.AutoField(max_length=16, verbose_name='项目id', primary_key=True,help_text='项目id')
    # user = models.ForeignKey(user, verbose_name='用户')
    project_name = models.CharField(max_length=20, default='', verbose_name='项目名称', help_text='项目名称')
    project_desc = models.TextField(default='', verbose_name='项目描述', help_text='项目描述')
    open_time = models.DateField(default=datetime.now, null=True, blank=True, verbose_name='项目开始日期', help_text='项目开始日期')
    close_time = models.DateField(default=datetime.now, null=True, blank=True, verbose_name='项目结束日期', help_text='项目结束日期')
    members = models.CharField(max_length=100, default='', blank=True, null=True, verbose_name='项目成员', help_text='项目成员')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project_name


class ModelManager(models.Model):
    """"
    模块管理
    """
    project = models.ForeignKey(ProjectManager, verbose_name='项目名称', help_text='项目名称')
    id = models.AutoField(max_length=16, verbose_name='模块id', primary_key=True, help_text='模块id')
    model_name = models.CharField(max_length=20, default='', null=True, blank=True, verbose_name='模块名称')
    parent_name = models.CharField(max_length=20, default='', null=True, blank=True, verbose_name='父模块名称', help_text='父模块名称')
    parent_id = models.IntegerField(default=1, verbose_name='父模块id', help_text='父模块id')
    # parent_name = models.ForeignKey("self", null=True, blank=True, verbose_name='父模块名称', help_text='父模块名称',
    #                                 related_name='sub_pro')
    # parent_id = models.ForeignKey("self", verbose_name='父模块id', help_text='父模块id', related_name='sub_id')
    models_desc = models.TextField(verbose_name='模块描述', help_text='模块描述')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '模块'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.model_name


class EnvManager(models.Model):
    """
    环境管理
    """
    TYPE_CHOICE = (
        (1, '开发环境'),
        (2, '测试环境'),
        (3, '预生产环境'),
        (4, '生产环境')
    )

    STATUS = ((0, '禁用'), (1, '可用'))

    env_name = models.CharField(max_length=10, default='', verbose_name='环境名称',help_text='环境名称')
    env_desc = models.TextField(verbose_name='环境描述', help_text='环境描述')
    env_type = models.IntegerField(default=1, choices=TYPE_CHOICE, verbose_name='环境类型', help_text='环境类型')
    host = models.CharField(max_length=30, default='', verbose_name='IP/域名',help_text='IP/域名')
    port = models.IntegerField(default=8080, verbose_name='端口', help_text='端口')
    env_status = models.IntegerField(default=1, choices=STATUS, verbose_name='环境是否可用',help_text='环境是否可用')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    env_info = UEditorField(verbose_name=u"环境信息", imagePath='base_config/imags',height=300,width=1000,filePath='base_config/files')

    class Meta:
        verbose_name = '环境'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.env_name

