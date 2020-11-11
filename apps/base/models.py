from django.db import models
from datetime import datetime
from DjangoUeditor.models import UEditorField
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.


class ProjectManager(models.Model):
    """
    项目
    """
    sn = models.CharField(max_length=16, verbose_name='项目编号',
                          null=True, blank=True, default='',  help_text='项目编号')
    # user = models.ForeignKey(user, verbose_name='用户')
    name = models.CharField(max_length=20, null=True, blank=True,
                            verbose_name='项目名称', help_text='项目名称')
    desc = models.TextField(default='', null=True, blank=True, verbose_name='项目描述', help_text='项目描述')
    open_time = models.DateField(default=datetime.now,
                                 null=True, blank=True, verbose_name='项目开始日期',
                                 help_text='项目开始日期')
    close_time = models.DateField(default='', null=True,
                                  blank=True, verbose_name='项目结束日期',
                                  help_text='项目结束日期')
    members = models.CharField(max_length=100, default='',
                               blank=True, null=True,
                               verbose_name='项目成员', help_text='项目成员')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    m_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = verbose_name
        db_table = "project_info"

    def __str__(self):
        return self.name


class ModelManager(models.Model):
    """"
    模块
    """
    parent_model = models.ForeignKey('self', null=True, blank=True, verbose_name='父模块名称',
                                     help_text='父模块名称',
                                     related_name='parent_leverl', on_delete=models.SET_NULL)
    project = models.ForeignKey(ProjectManager, blank=True, null=True, on_delete=models.CASCADE, verbose_name='项目名称', help_text='项目名称')
    name = models.CharField(max_length=20, default='', null=True, blank=True, verbose_name='模块名称')
    desc = models.TextField(verbose_name='模块描述', help_text='模块描述', null=True, blank=True,)
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    model_owner = models.ManyToManyField(User, verbose_name='模块负责人',
                                    help_text='模块负责人', blank=True,)
    m_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '模块'
        verbose_name_plural = verbose_name
        db_table = "model_info"

    def __str__(self):
        return self.name


class EnvManager(models.Model):
    """
    环境
    """
    TYPE_CHOICE = (
        (1, '开发环境'),
        (2, '测试环境'),
        (3, '预生产环境'),
        (4, '生产环境')
    )

    STATUS = ((1, '禁用'), (2, '可用'))

    name = models.CharField(max_length=10, default='', verbose_name='环境名称', help_text='环境名称')
    desc = models.TextField(verbose_name='环境描述', null=True, blank=True,help_text='环境描述')
    type = models.IntegerField(default=1, choices=TYPE_CHOICE,  null=True, blank=True,
                               verbose_name='环境类型', help_text='环境类型')
    host = models.CharField(max_length=126, default='',  null=True, blank=True,
                            verbose_name='IP/域名', help_text='IP/域名')
    port = models.IntegerField(default=8080,  null=True, blank=True,
                               verbose_name='端口', help_text='端口')
    status = models.IntegerField(default=1, choices=STATUS,  null=True,
                                 blank=True, verbose_name='环境是否可用', help_text='环境是否可用')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    # info = UEditorField(verbose_name=u"环境信息", imagePath='base/imags', height=300, width=1000,
    #                         filePath='base/files')
    m_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '环境'
        verbose_name_plural = verbose_name
        db_table = 'environment_info'

    def __str__(self):
        return self.name


class ProjectDynamic(models.Model):
    """
    项目动态
    """
    time = models.DateTimeField(auto_now=True, verbose_name='操作时间')
    types = models.CharField(max_length=50, verbose_name='操作类型')
    operationObject = models.CharField(max_length=50, verbose_name='操作对象')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,related_name='userName', verbose_name='操作人')
    description = models.CharField(max_length=1024, blank=True, null=True,  verbose_name='描述')

    def __str__(self):
        return self.types

    class Meta:
        verbose_name = '项目动态'
        verbose_name_plural = '项目动态'
        db_table = "project_dynamic"


class ProjectMemebers(models.Model):
    """
    项目成员
    """
    project = models.ForeignKey(ProjectManager, null=True, blank=True, on_delete=models.CASCADE,
                                verbose_name="所属项目")
    user = models.ForeignKey(User, null=True, blank=True, verbose_name="用户",on_delete=models.CASCADE)

    def __str__(self):
        return "%s%s".format(self.project, self.user)

    class Meta:
        verbose_name = '项目成员'
        verbose_name_plural = verbose_name
        db_table = "project_memebers"
