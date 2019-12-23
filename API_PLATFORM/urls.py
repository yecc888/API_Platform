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
import xadmin
from rest_framework.routers import DefaultRouter
from API_PLATFORM.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from base_config.views import EnvsListViewSet, ProjectViewSet
from users.views import UserViewSet
from rest_framework.authtoken import views
from django.views.generic.base import TemplateView
from rest_framework_jwt.views import obtain_jwt_token
import DjangoUeditor
from django.conf.urls.static import static
from API_PLATFORM import settings
# from django.contrib import admin

router = DefaultRouter()
# 配置环境管理页的url
router.register(r'envs', EnvsListViewSet, base_name='envs')
router.register(r'projects', ProjectViewSet, base_name='projects')
router.register(r'users', UserViewSet, base_name='users')
# router.register(r'addusers', AddUserViewSet, base_name='addusers')



# 手动配置
# envs_list = EnvsListViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # url(r'^envs/$', envs_list, name="env-list"),
    # 通过路由配置
    url(r'^api/', include(router.urls)),
    url(r'docs/', include_docs_urls(title='接口测试平台接口文档')),
    url(r'^api-auth/', include('rest_framework.urls')),
    # drf自带的token 认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),
    # jwt认证接口
    url(r'^api/login/', obtain_jwt_token, name='login'),
    url(r'^$', TemplateView.as_view(template_name='index.html')),  #2、 增加该行
    # url(r'ueditor/', include('DjangoUeditor.utils'))

 ]
