from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from uuid import uuid4


# Create your models here.


class UserProfile(AbstractUser):
    """
    用户
    """
    ROLE_CHOICE = ((1, '测试人员'),
                   (2, '开发人员'))
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='用户名')
    # password = models.CharField(max_length=20000, null=True, blank=True, verbose_name='密码')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='邮箱')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    user_roles = models.IntegerField(default=1, choices=ROLE_CHOICE, verbose_name='用户角色', help_text='用户角色')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    id = models.AutoField(max_length=16, verbose_name='用户id', primary_key=True, help_text='用户id')
    user_secret = models.UUIDField(default=uuid4, verbose_name='用户jwt加密秘钥')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username


class sidebarInfo(models.Model):
    """
    动态展示侧边栏，与前端配合
    """
    parentId = models.SmallIntegerField(default=0, verbose_name='父组件ID')
    title = models.CharField(max_length=12, default='', verbose_name='导航名称')
    level = models.SmallIntegerField(default=0, verbose_name='等级')
    sort = models.SmallIntegerField(default=0, verbose_name='排序')
    name = models.CharField(max_length=12, default='', verbose_name='vue组件名称')
    icon = models.CharField(max_length=20, default='', verbose_name='图标')
    hidden = models.SmallIntegerField(default=0, verbose_name='是否隐藏')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '侧边栏'
        verbose_name_plural = '侧边栏'
        db_table = 'sidebarinfo'

    def __str__(self):
        return "{0}{1}".format(self.title, self.name)


class useInfo(models.Model):
    """
    用户导航
    """
    role = models.CharField(max_length=12, default='TEST', verbose_name='角色')
    icon = models.ImageField(upload_to="icon/images/", null=True, blank=True, verbose_name="头像")
    menus = models.ManyToManyField(sidebarInfo, verbose_name='导航内容')
    user = models.ForeignKey(UserProfile,null=True,blank=True, default=1,verbose_name="用户", on_delete=models.CASCADE)

    class Meta:
        verbose_name = '用户导航'
        verbose_name_plural = '用户导航'
        db_table = "useinfo"

    def __str__(self):
        return self.role
