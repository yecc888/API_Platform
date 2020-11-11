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
    list_display = ["name", "desc", "create_time"]
    search_fields = ['name', ]
    list_editable = ["name", ]
    list_filter = ["name", "desc", "create_time"]


class EnvAdmin(object):
    list_display = ["name", "type", "host", "port", "status", "create_time"]
    search_fields = ['name', ]
    list_editable = ["name", ]
    list_filter = ["name", "type", "host", "port", "status", "create_time"]


class ModelAdmin(object):
    list_display = ["project", "id", "name", "parent_model", "create_time"]
    search_fields = ['name', ]
    list_editable = ["name", ]
    list_filter = ["project", "id", "name", "parent_model", "create_time"]


# xadmin.site.unregister(ProjectManager)
xadmin.site.register(ProjectManager, ProjectAdmin)
xadmin.site.register(EnvManager, EnvAdmin)
xadmin.site.register(ModelManager, ModelAdmin)
