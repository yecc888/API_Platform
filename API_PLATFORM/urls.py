"""API_PLATFORM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.urls import path
import xadmin
from rest_framework.routers import DefaultRouter
from API_PLATFORM.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from django.views.generic.base import TemplateView
from rest_framework_jwt.views import obtain_jwt_token
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from apps.users.forms import MyAuthenticationForm

from base.views import EnvsListViewSet, ProjectViewSet, ModelViewSet, ProjectDynamicViewSet
from users.views import UserViewSet, obtain_jwt_token1, UserInfoView, UserInfoView1, Logout
from cases.views import InterfaceManagermentViewSet, HeaderTempViewSet, CustomParametersViewSet, ApiMockViewSet
from cases.views import SendRequest, MockRuestView, CaseApiViewSet, CaseGroupViewSet, \
    CaseViewSet,ApiResponseViewSet, GetApiResponseViewSet
import DjangoUeditor
from django.conf.urls.static import static
from API_PLATFORM import settings

from django.contrib import admin

router = DefaultRouter()
# 配置环境管理页的url
router.register(r'envs', EnvsListViewSet, base_name='envs')
# 配置项目管理url
router.register(r'projects', ProjectViewSet, base_name='projects')
router.register(r'projectdynamic', ProjectDynamicViewSet, base_name='projectdynamic')
# 配置用户url
router.register(r'users', UserViewSet, base_name='users')
# 配置模块url
router.register(r'models', ModelViewSet, base_name='models')
# 接口相关url配置
router.register(r'interface', InterfaceManagermentViewSet, base_name='interface')
# router.register(r'interface_results', InterfaceResultsViewSet, base_name='interface_results')

router.register(r'headertemp', HeaderTempViewSet, base_name='headertemp')
# 配置导航
router.register(r'admin/info', UserInfoView1, base_name='admin-info')
# 接口调试
router.register(r'send', SendRequest, base_name='send')
# 自定义变量
router.register(r'custom/parameters', CustomParametersViewSet, base_name='custom-parameters')
# mock接口配置
router.register(r'mockinfo', ApiMockViewSet, base_name='mock-info')
# 测试用例配置
router.register(r'case', CaseViewSet, base_name='case')

# 用例分组配置
router.register(r'caseGroup', CaseGroupViewSet, base_name='caseGroup')

# 用例接口配置
router.register(r'caseApi', CaseApiViewSet, base_name='caseApi')

# 接口历史信息配置
router.register(r'apiHistory', ApiResponseViewSet, base_name='apiHistory')

# 接口历史信息配置
router.register(r'getApiResp', GetApiResponseViewSet, base_name='getApiResp')

# 手动配置
# envs_list = EnvsListViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })


schema_view = get_schema_view(
    openapi.Info(
        title="API-TESTING API",
        default_version='v1',
        description='<h3>接口文档，请使用管理员登录后，使用该文档，否则无权限访问接口</h3>'
                    ' <br> The swagger YAML document can be found '
                    '<a rel="noopener noreferrer" target="_blank" '
                    'href="/swagger.yaml"> here</a>',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# schema_view1 = get_swagger_view(title='接口文档')

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # media 配置
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 通过路由配置
    url(r'^api/', include(router.urls)),
    url(r'docs/', include_docs_urls(title='接口测试平台接口文档')),
    # url(r'swagger-ui/', schema_view1),
    url(r'^api-auth/', include('rest_framework.urls')),
    # drf自带的token 认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt认证接口
    url(r'^api/login', obtain_jwt_token, name='login'),
    url(r'^api/logout', Logout.as_view()),
    # url(r'admin/info',UserInfoView.as_view()),
    # 前后端分离，前端入口页面配置
    url(r'^$', TemplateView.as_view(template_name='index.html')),  # 2、 增加该行
    # url(r'ueditor/', include('DjangoUeditor.utils'))

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # swagga 登录/登出配置
    url(r'accounts/login/', LoginView.as_view(template_name="swagga-index.html",
                                              authentication_form=MyAuthenticationForm), name='login'),
    url(r'accounts/logout/', LogoutView.as_view(), name='logout'),
    url(r'mock/(.*)', MockRuestView.as_view()),
    #url(r'apiresp/(.*)', GetApiResponseView.as_view()),

    # url(r'^admin/', admin.site.urls),
    # url(r'api/send/', SendRequest.as_view())

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
