__author__ = 'yecc'
__date__ = '2020/4/8 21:20'

from django.db.models.signals import post_save, post_delete
from .models import ProjectManager, ProjectDynamic, ModelManager,EnvManager
from django.dispatch import receiver
from django.db import transaction

from django.contrib.auth import get_user_model
from users.views import get_users
from .utils import record_dynamic

user = get_user_model()


# 参数一接收哪种信号，参数二是接收哪个model的信号
@transaction.atomic
@receiver(post_save, sender=ModelManager)
def model_record(sender, instance=None, created=False, **kwargs):
    """
    动态记录模块类的操作信息
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # 是否新建，因为update的时候也会进行post_save
    if created:
        record_dynamic(types="新增", operation_object="模块",
                       user=1,
                       description=instance.name)
    else:
        record_dynamic(types="更新", operation_object="模块",
                       user=1,
                       description=instance.name)


@receiver(post_delete, sender=ModelManager)
def model_record_del(sender, instance=None, created=False, **kwargs):
    """
        动态记录模块类的操作信息
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # 是否新建，因为update的时候也会进行post_save
    record_dynamic(types="删除", operation_object="模块",
                   user=1,
                   description=instance.name)


# 参数一接收哪种信号，参数二是接收哪个model的信号
@receiver(post_save, sender=EnvManager)
def env_record(sender, instance=None, created=False, **kwargs):
    """
    动态记录环境类的操作信息
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # 是否新建，因为update的时候也会进行post_save
    if created:
        record_dynamic(types="新增", operation_object="环境",
                       user=1,
                       description=instance.name)
    else:
        record_dynamic(types="更新", operation_object="环境",
                       user=1,
                       description=instance.name)


@receiver(post_delete, sender=EnvManager)
def env_record_del(sender, instance=None, created=False, **kwargs):
    """
        动态记录环境类的操作信息
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # 是否新建，因为update的时候也会进行post_save
    record_dynamic(types="删除", operation_object="环境",
                   user=1,
                   description=instance.name)


# 参数一接收哪种信号，参数二是接收哪个model的信号
@receiver(post_save, sender=ProjectManager)
def pro_record(sender, instance=None, created=False, **kwargs):
    """
    动态记录环境类的操作信息
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # 是否新建，因为update的时候也会进行post_save
    if created:
        record_dynamic(types="新增", operation_object="项目",
                       user=1,
                       description=instance.name)
    else:
        record_dynamic(types="更新", operation_object="项目",
                       user=1,
                       description=instance.name)


@receiver(post_delete, sender=ProjectManager)
def pro_record_del(sender, instance=None, created=False, **kwargs):
    """
        动态记录环境类的操作信息
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # 是否新建，因为update的时候也会进行post_save
    record_dynamic(types="删除", operation_object="项目",
                   user=1,
                   description=instance.name)
