__author__ = 'yecc'
__date__ = '2019/12/20 10:27'

import re
from django.contrib.auth import get_user_model
from API_PLATFORM.settings import REGEX_MOBILE

User = get_user_model()


def jwt_response_payload_handler(token, user=None, request=None):
    """为返回的结果添加用户相关信息"""

    return {
        'Token': token,
        'user_id': user.id,
        'username': user.username}


def get_user(account):
    """
    通过手机号、邮箱登录
    :param account:
    :return:
    """
    try:
        if re.match(REGEX_MOBILE, account):
            user = User.objects.get(mobile=account)
        elif "@" in str(account):
            user = User.objects.get(email=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


if __name__ == "__main__":
    print(re.match(REGEX_MOBILE,'1358444466'))