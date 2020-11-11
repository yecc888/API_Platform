__author__ = 'yecc'
__date__ = '2020/4/10 17:41'

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UserProfile
from django.contrib.auth import get_user_model
from users.views import get_users
from base.utils import record_dynamic


# 参数一接收哪种信号，参数二是接收哪个model的信号
@receiver(post_save, sender=UserProfile)
def user_record(sender, instance=None, created=False, **kwargs):
    """
    动态记录用户类的操作信息
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # 是否新建，因为update的时候也会进行post_save
    if created:
        record_dynamic(types="新增", operation_object="用户",
                       user=1,
                       description=instance.username)
    else:
        record_dynamic(types="更新", operation_object="用户",
                       user=1,
                       description=instance.username)


@receiver(post_delete, sender=UserProfile)
def user_record_del(sender, instance=None, created=False, **kwargs):
    """
        动态记录用户类的操作信息
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # 是否新建，因为update的时候也会进行post_save
    record_dynamic(types="删除", operation_object="用户",
                   user=1,
                   description=instance.username)
