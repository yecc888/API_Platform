__author__ = 'yecc'
__date__ = '2020/4/8 18:29'

import logging
from datetime import datetime
from .models import ProjectDynamic, ProjectManager
from .serializers import ProjectDynamicDeserializer

logger = logging.getLogger(__name__)


def record_dynamic(types, operation_object, user, description):
    """
    记录项目动态信息
    :param types:  操作类型（增删改）
    :param operation_object: 操作对象
    :param description: 内容
    :return:
    """
    times = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dynamic_serializer = ProjectDynamicDeserializer(
        data={"types": types,
              "time": times,
              "operationObject": operation_object,
              "description": description,
              "user": user
              })
    try:
        if dynamic_serializer.is_valid():
            dynamic_serializer.save()
    except Exception as ex:
        logger.error(str(ex))


if __name__ == "__main__":
    record_dynamic(1,"rr","rrr","eeer")
