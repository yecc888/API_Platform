from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
import demjson,json,time,importlib,os
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
from rest_framework.views import APIView

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from base.views import BasePagination
from .filter import ApiFilter,HeaderTempFilter, CustomParaFilter, ApiMockFilter
from .httpMethods import send
from .utils import make_custom_file,impt
from .models import AllHeaders,ApiManagerment,ApiParams, ApiResponse, \
    Headers,CustomParameters,ApiMock,CaseApi,CaseGroup,CaseManagerment, CustomFunc

from .serializers import ApiManagermentDeserializer, \
    ApiManagermentSerializer,HeadersSerializer,ParamarsSerializer, \
    HeaderTempDeserializer,HeaderTempSerializer,ApiTestSerializer,CustomParametersSerializer, \
    ApiMockSerializer, CaseSerializer,CaseApiSerializer,CaseGroupSerializer, \
    CaseApiDeserializer,ApiResponseSerializer,CaseDeserializer, CaseGroupDserializer,CustomFuncSerializer


class CustomFuncViewSet(viewsets.ModelViewSet):
    """
    自定义函数
    list:
        根据fileName返回查询的数据
    create:
        创建
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = CustomFunc.objects.all()
    pagination_class = BasePagination
    serializer_class = CustomFuncSerializer
    ordering = ['id']

# def get_object(self):
    #     obj = self.request.query_params.get('fileName')
    #     return obj
    def get_queryset(self):
        fileName = self.request.query_params.get('fileName')
        queryset = CustomFunc.objects.filter(fileName=fileName)
        return queryset

    def list(self, request, *args, **kwargs):

        fileName = self.request.query_params.get('fileName')
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            if queryset:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            else:
                # return Response(data=[f'{fileName},函数文件不存在,请先创建！'])
                return self.get_paginated_response({f'{fileName},函数文件不存在,请先创建！'})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EditCustomFuncViewSet(viewsets.ModelViewSet):
    """
    自定义函数
    put:
        更新
    deleter:
        删除
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = CustomFunc.objects.all()
    pagination_class = BasePagination
    serializer_class = CustomFuncSerializer
    ordering = ['id']


class DeBugCustomFuncView(APIView):
    """
    调试自定义
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self,request):
        data = dict(request.POST)
        py_id = int((data.get('fileId')[0]))
        func_name_or_p = data.get('funName')[0]
        if not py_id:
            return Response('请先加载函数文件')
        if not func_name_or_p:
            return Response('请输入调试的函数和参数')
        try:
            func_data = CustomFunc.objects.get(id=py_id)
            all_data = CustomFuncSerializer(instance=func_data).data
            make_custom_file(all_data['fileName'],all_data['content'])
        except ObjectDoesNotExist as ex:
            raise
        # model = all_data['fileName'].rstrip('.py')
        # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # pg = os.path.join(BASE_DIR,'customfunc')
        # mod = importlib.
        # import_module(model,package=pg)
        mod = impt(all_data)
        print(mod)







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

    def get_serializer_class(self):
        if self.action in ["list", 'retrieve']:
            return CaseSerializer
        elif self.action == "create":
            return CaseDeserializer
        return CaseSerializer


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
    # queryset = CaseGroup.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    serializer_class = CaseGroupSerializer

    def get_serializer_class(self):

        if self.action in ["list", 'retrieve']:
            return CaseGroupSerializer
        elif self.action == "create":
            return CaseGroupDserializer
        return CaseGroupDserializer

    def get_queryset(self):
        # 如果已经存在父级，则不展示
        queryset = CaseGroup.objects.filter(group=None)
        return queryset


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
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    # authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    # serializer_class = CaseApiDeserializer
    queryset = CaseApi.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", 'retrieve']:
            return CaseApiSerializer
        elif self.action == "create":
            return CaseApiDeserializer
        return CaseApiDeserializer

    # def get_queryset(self):
    #     api_id = self.request.query_params.get('caseId', 0)
    #     queryset = CaseApi.objects.filter(case_id=int(api_id))
    #     return queryset














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
