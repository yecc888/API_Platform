__author__ = 'yecc'
__date__ = '2020/5/4 12:17'

import django
import sys
import os


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
PathProject = os.path.split(rootPath)[0]
sys.path.append(rootPath)
sys.path.append(PathProject)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "API_PLATFORM.settings")
django.setup()

import json
import logging
import re

logger = logging.getLogger(__name__)
logger.info('dfsdfs')
logger.error('errrrwors')