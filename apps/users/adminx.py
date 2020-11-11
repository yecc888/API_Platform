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
# from .models import VerifyCode
from .models import UserProfile, useInfo, sidebarInfo


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "接口管理后台"
    site_footer = "API_TEST"
    # menu_style = "accordion"


class UsersAdmin(object):
    list_display = ['name', 'mobile', "create_time"]


class UserinfoAdmin(object):
    list_display = ['icon', 'menus']


class SidebarInfoAdmin(object):
    list_display = ['parentId', 'title', 'level', 'sort', 'name', 'icon','hidden', "createTime"]


xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile, UsersAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(useInfo, UserinfoAdmin)
xadmin.site.register(sidebarInfo, SidebarInfoAdmin)
