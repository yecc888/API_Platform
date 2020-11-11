from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
import demjson,json,time
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from rest_framework.parsers import JSONParser,MultiPartParser,FormParser,BaseParser
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import AllHeaders,ApiManagerment,ApiParams, ApiResponse, \
    Headers,CustomParameters,ApiMock,CaseApi,CaseGroup,CaseManagerment
from .serializers import ApiManagermentDeserializer, \
    ApiManagermentSerializer,HeadersSerializer,ParamarsSerializer, \
    HeaderTempDeserializer,HeaderTempSerializer,ApiTestSerializer,CustomParametersSerializer, \
    ApiMockSerializer, CaseSerializer,CaseApiSerializer,CaseGroupSerializer, CaseApiDeserializer,ApiResponseSerializer
from base.views import BasePagination
from .filter import ApiFilter,HeaderTempFilter, CustomParaFilter, ApiMockFilter
from rest_framework.views import APIView
from .httpMethods import send


class InterfaceManagermentViewSet(viewsets.ModelViewSet):
    """
    list:
        获取接口列表
    create:
        创建接口
    delete:
        删除接口
    update:
        更新接口
    """

    pagination_class = BasePagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = ApiManagerment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['create_time', 'name']
    ordering = ['-m_time']
    filter_class = ApiFilter

    def get_serializer_class(self):
        if self.action in ["list", 'retrieve']:
            return ApiManagermentSerializer
        elif self.action == "create":
            return ApiManagermentDeserializer
        return ApiManagermentDeserializer


class HeaderTempViewSet(viewsets.ModelViewSet):
    """
    list:
        获取Header列表
    create:
        创建Header
    delete:
        删除Header
    update:
        更新Header
    """

    pagination_class = BasePagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = Headers.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['create_time', 'name']
    ordering = ['-m_time']
    filter_class = HeaderTempFilter


    def get_serializer_class(self):
        if self.action in ["list", 'retrieve']:
            return HeaderTempDeserializer
        elif self.action == "create":
            return HeaderTempSerializer
        return HeaderTempSerializer


class SendRequest(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    执行快速测试
    """
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = ApiManagerment.objects.all()
    serializer_class = ApiTestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        test_data = request.data
        global times
        times = ''
        try:
            status_code, response_header, response_content,times = send(test_data)
        # self.perform_create(serializer)
        except Exception as ex:
            return Response(data={"status_code": 400, "response_header": {}, "response_content": {"errMsg":str(ex)},"time":0})
        else:
            return Response(data={"status_code":status_code,"response_header":response_header,"response_content":response_content,"time":times})




class GetApiResponseViewSet(viewsets.ModelViewSet):
    """
       list:获取某个接口的所有历史请求信息
    """

    pagination_class = BasePagination
    serializer_class = ApiResponseSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    ordering_fields = ['create_time',]
    ordering = ['-create_time']
    # def get_object(self):
    #     api_id = self.request.query_params.get('apiId',0)

    def get_queryset(self):
        api_id = self.request.query_params.get('apiId',0)
        queryset = ApiResponse.objects.filter(api_id=int(api_id))
        return queryset


class ApiResponseViewSet(viewsets.ReadOnlyModelViewSet):
    """
        list:
        获取所有接口历史信息,暂时废弃
    """
    pagination_class = BasePagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = ApiResponse.objects.all()
    ordering = ['-create_time']
    serializer_class = ApiResponseSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CustomParametersViewSet(viewsets.ModelViewSet):
    """
    list:
        获取CustomParameters列表
    create:
        创建CustomParameters
    delete:
        删除CustomParameters
    update:
        更新CustomParameters
    """
    pagination_class = BasePagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = CustomParameters.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['create_time', 'name']
    ordering = ['-m_time']
    serializer_class = CustomParametersSerializer
    filter_class = CustomParaFilter


class ApiMockViewSet(viewsets.ModelViewSet):
    """
    mock接口
    list:
        获取ApiMock列表
    create:
        创建ApiMock
    delete:
        删除ApiMock
    update:
        更新ApiMock
    """
    pagination_class = BasePagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = ApiMock.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['create_time', 'name']
    ordering = ['-m_time']
    serializer_class = ApiMockSerializer
    filter_class = ApiMockFilter


class PlainTextParser(BaseParser):
    """
    Plain text 解析器。
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        只需返回一个表示请求正文的字符串。
        """
        return stream.read()


class MockRuestView(APIView):
    """
    Mock,接口
    """
    permission_classes = ()
    authentication_classes = ()
    parser_classes = (JSONParser,MultiPartParser,FormParser,PlainTextParser)

    def get(self,request,path):
        """
        get,mock接口返回没内容
        :param request:
        :param path:
        :return:
        """
        if path:
            param = dict(request.query_params)
            for key,value in param.items():
                param.update({key:value[0]})
            try:
                objs = ApiMock.objects.get(url=path, method='GET')
            except ObjectDoesNotExist:
                return Response(data={"errMsg": "Mock接口不存在，请先添加", "errCode": -1})
            if objs.status == 2:
                return Response(data={"errMsg": "Mock接口已禁用，请先启用", "errCode": 0})
            if param and objs.mock_param:
                for key in param.keys():
                    if key not in demjson.decode(objs.mock_param).keys():
                        return Response(data={"errMsg": "Mock接口不存在，请先添加", "errCode": -1})
            objs.mock_times += 1
            objs.save()
            # 延迟返回结果
            if objs.delay:
                time.sleep(float(objs.delay))
            if "{" in objs.response_content:
                return Response(data=demjson.decode(objs.response_content))
            else:
                return Response(data=objs.response_content)
        else:
            return Response(data={"errMsg": "Mock路径错误", "errCode": -1})

    def post(self,request,path):
        """
        post,mock接口返回没内容
        :param request:
        :param path:
        :return:
        """
        if path:
            content_type = request.content_type
            if content_type == 'application/x-www-form-urlencoded':
                body_data = dict(request.data)
                for key, value in body_data.items():
                    body_data.update({key: value[0]})
            elif content_type == 'application/json':
                body_data = request.data
            else:
                return Response(data={"errMsg": "请输入Header,Content-Type"})
            try:
                objs = ApiMock.objects.get(url=path, method='POST')
            except ObjectDoesNotExist:
                return Response(data={"errMsg": "Mock接口不存在，请先添加", "errCode": -1})
            # 接口禁用判断
            if objs.status == 2:
                return Response(data={"errMsg": "Mock接口已禁用，请先启用", "errCode": 0})
            # 存在请求体判断
            if body_data and objs.mock_bodys:
                for key in body_data.keys():
                    if key not in demjson.decode(objs.mock_bodys).keys():
                        return Response(data={"errMsg": "Mock接口不存在，请先添加", "errCode": -1})
            # 统计mock次数
            objs.mock_times += 1
            objs.save()
            # 延迟返回结果
            if objs.delay:
                time.sleep(float(objs.delay))

            if "{" in objs.response_content:
                return Response(data=demjson.decode(objs.response_content))
            else:
                return Response(data=objs.response_content)
        else:
            return Response(data={"errMsg": "Mock路径错误", "errCode": -1})


class CaseViewSet(viewsets.ModelViewSet):
    """
    list:
        获取用例列表
    create:
        创建用例
    delete:
        删除用例
    update:
        更新用例
    """
    pagination_class = BasePagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = CaseManagerment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['create_time', 'name']
    ordering = ['-m_time']
    serializer_class = CaseSerializer
    # filter_class = ApiMockFilter


class CaseGroupViewSet(viewsets.ModelViewSet):
    """
    list:
        获取用例分组列表
    create:
        创建用例分组
    delete:
        删除用例分组
    update:
        更新用例分组
    """
    pagination_class = BasePagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = CaseGroup.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    serializer_class = CaseGroupSerializer
    # filter_class = ApiMockFilter


class CaseApiViewSet(viewsets.ModelViewSet):
    """
    list:
        获取用例接口列表
    create:
        创建用例接口
    delete:
        删除用例接口
    update:
        更新用例接口
    """
    pagination_class = BasePagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = CaseApi.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    # serializer_class = CaseApiSerializer
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    # filter_class = ApiMockFilter


    def get_serializer_class(self):
        if self.action in ["list", 'retrieve']:
            return CaseApiDeserializer
        elif self.action == "create":
            return CaseApiSerializer
        return CaseApiDeserializer














#################################################
# 实例化调度器
# scheduler = BackgroundScheduler()
# # 调度器使用默认的DjangoJobStore()
# scheduler.add_jobstore(DjangoJobStore(), 'default')
#
# # 每天8点半执行这个任务
# @register_job(scheduler, 'cron', id='test', hour=11, minute=20 , args=['test'])
# def test(s):
#     # 具体要执行的代码
#     print('dfdfdf')
#
# # 注册定时任务并开始
# register_events(scheduler)
# scheduler.start()