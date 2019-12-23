#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: liyao
@license: Apache Licence
@contact: yli@posbao.net
@site: http://www.piowind.com/
@software: PyCharm
@file: adminx.py
@time: 2017/7/4 17:04
"""
import xadmin
from xadmin import views
from .models import ProjectManager, EnvManager, ModelManager


class ProjectAdmin(object):
    list_display = ["project_name", "project_desc", "create_time"]
    search_fields = ['project_name', ]
    list_editable = ["project_name", ]
    list_filter = ["project_name", "project_desc", "create_time"]


class EnvAdmin(object):
    list_display = ["env_name", "env_type", "host", "port", "env_status", "create_time"]
    search_fields = ['env_name', ]
    list_editable = ["env_name", ]
    list_filter = ["env_name", "env_type", "host", "port", "env_status", "create_time"]


class ModelAdmin(object):
    list_display = ["project", "id", "model_name", "parent_name", "parent_id", "create_time"]
    search_fields = ['model_name', ]
    list_editable = ["model_name", ]
    list_filter = ["project", "id", "model_name", "parent_name", "parent_id", "create_time"]


# xadmin.site.unregister(ProjectManager)
xadmin.site.register(ProjectManager, ProjectAdmin)
xadmin.site.register(EnvManager, EnvAdmin)
xadmin.site.register(ModelManager, ModelAdmin)
