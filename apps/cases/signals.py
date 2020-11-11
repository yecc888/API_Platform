__author__ = 'yecc'
__date__ = '2020/4/10 17:41'

from django.db.models.signals import post_save, post_delete
from .models import ApiManagerment,CustomParameters
from django.dispatch import receiver
from django.db import transaction

from django.contrib.auth import get_user_model
from users.views import get_users
from base.utils import record_dynamic

user = get_user_model()


# 参数一接收哪种信号，参数二是接收哪个model的信号
@transaction.atomic
@receiver(post_save, sender=ApiManagerment)
def api_record(sender, instance=None, created=False, **kwargs):
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
        record_dynamic(types="新增", operation_object="接口",
                       user=1,
                       description=instance.name)
    else:
        record_dynamic(types="更新", operation_object="接口",
                       user=1,
                       description=instance.name)


@receiver(post_delete, sender=ApiManagerment)
def api_record_del(sender, instance=None, created=False, **kwargs):
    """
        动态记录模块类的操作信息
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # 是否新建，因为update的时候也会进行post_save
    record_dynamic(types="删除", operation_object="接口",
                   user=1,
                   description=instance.name)


# 参数一接收哪种信号，参数二是接收哪个model的信号
@transaction.atomic
@receiver(post_save, sender=CustomParameters)
def cp_record(sender, instance=None, created=False, **kwargs):
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
        record_dynamic(types="新增", operation_object="自定义参数",
                       user=1,
                       description=instance.name)
    else:
        record_dynamic(types="更新", operation_object="自定义参数",
                       user=1,
                       description=instance.name)


@receiver(post_delete, sender=CustomParameters)
def api_record_del(sender, instance=None, created=False, **kwargs):
    """
        动态记录模块类的操作信息
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # 是否新建，因为update的时候也会进行post_save
    record_dynamic(types="删除", operation_object="自定义参数",
                   user=1,
                   description=instance.name)