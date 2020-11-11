__author__ = 'yecc'
__date__ = '2020/3/30 17:02'

import xadmin
from .models import ApiManagerment,ApiResponse,ApiParams,Headers,CustomParameters


class InterfaceManagermentAdmin(object):
    list_display = ["name", "url", "method","status"]
    search_fields = ["name"]
    list_editable = ["name"]
    list_filter = ["name", "url", "method","status"]


class InterfaceParasAdmin(object):
    list_display = ["name", "header", "raw"]
    search_fields = ["name"]
    list_editable = ["name"]
    list_filter = ["name"]


class InterfaceResultsAdmin(object):
    list_display = ["name", "status_code", "success_num", "fail_num"]
    search_fields = ["name", "status_code", "success_num", "fail_num"]
    list_editable = ["name", "status_code", "success_num", "fail_num"]
    list_filter = ["name", "status_code", "success_num", "fail_num"]


class CaseManagermentAdmin(object):
    list_display = ["name"]
    search_fields = ["name"]
    list_editable = ["name"]
    list_filter = ["name"]

class CaseResultAdmin(object):
    list_display = ["name","status_code"]
    search_fields = ["name"]
    list_editable = ["name"]
    list_filter = ["name"]


class HeaderTempAdmin(object):
    list_display = ["name","value"]
    search_fields = ["name"]
    list_editable = ["name"]
    list_filter = ["name"]

class CustomParametersAdmin(object):
    list_display = ["name","key","value"]
    search_fields = ["name"]
    list_editable = ["name"]
    list_filter = ["name"]


xadmin.site.register(ApiManagerment, InterfaceManagermentAdmin)
xadmin.site.register(CustomParameters, CustomParametersAdmin)
xadmin.site.register(ApiParams, InterfaceParasAdmin)
xadmin.site.register(Headers, HeaderTempAdmin)

# xadmin.site.register(CaseManagerment, CaseManagermentAdmin)
# xadmin.site.register(CaseResult, CaseResultAdmin)
