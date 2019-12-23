__author__ = 'yecc'
__date__ = '2019/11/29 14:18'

import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+'../')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "API_PLATFORM.settings")
import django
django.setup()
from users.models import UserProfile
users = UserProfile.objects.all()
print(users)