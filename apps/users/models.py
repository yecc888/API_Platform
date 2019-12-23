from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
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
    user_roles = models.IntegerField(default=1, choices=ROLE_CHOICE, verbose_name='用户角色',help_text='用户角色')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    id = models.AutoField(max_length=16, verbose_name='用户id', primary_key=True,help_text='用户id')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username
