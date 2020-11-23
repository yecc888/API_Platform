from django.db import models
import uuid
from django.contrib.auth import get_user_model
from base.models import ModelManager, EnvManager
import datetime

# Create your models here.
User = get_user_model()


class BaseModel(models.Model):
    """
    基础 model，抽象类型，可以继承，不会创建表
    """
    m_time = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
        help_text='更新时间')
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
        help_text='创建时间')

    class Meta:
        abstract = True


class Group(models.Model):
    """
    分组
    """
    name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="分组名称")
    group = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name="上级分组",
        related_name='group')

    class Meta:
        abstract = True


class Headers(BaseModel):
    """接口模板"""
    name = models.CharField(
        max_length=124,
        default='',
        verbose_name='Header名称')
    value = models.CharField(
        max_length=124,
        default='',
        verbose_name='Header值')
    add_user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name='添加人')

    class Meta:
        verbose_name = '接口模板'
        verbose_name_plural = verbose_name
        db_table = 'header_template'

    def __str__(self):
        return "{}:{}".format(self.name, self.value)


class ApiManagerment(models.Model):
    """
    接口
    """
    # 方法类型
    METHOD_TPYE = (('GET', 'GET'),
                   ('POST', 'POST'),
                   ('DELETE', 'DELETE'),
                   ('PUT', 'PUT'),
                   ('PATCH', 'PATCH'),
                   ('HEAD', 'HEAD'),
                   ('OPTIONS', 'OPTIONS'))
    # 协议类型
    PROTOCOL_TPYE = (('HTTP', 'HTTP'),
                     ('HTTPS', 'HTTPS'))
    # 接口状态
    INTTERFACE_STATUS = ((1, '可用'),
                         (2, '禁用'))
    # 是否加密接口
    SIGN = ((1, '不加密'),
            (2, '加密'))

    env = models.ForeignKey(
        EnvManager,
        null=True,
        blank=True,
        verbose_name="所属环境",
        help_text="所属环境",
        on_delete=models.SET_NULL)
    model = models.ForeignKey(
        ModelManager,
        null=True,
        blank=True,
        verbose_name='模块名称',
        on_delete=models.SET_NULL)
    name = models.CharField(
        max_length=20,
        default='',
        null=True,
        blank=True,
        verbose_name='接口名称',
        help_text='接口名称')
    url = models.CharField(
        max_length=100,
        default='',
        null=True,
        blank=True,
        verbose_name='接口路径',
        help_text='接口路径')
    protocol = models.CharField(
        max_length=10,
        default='HTTP',
        choices=PROTOCOL_TPYE,
        null=True,
        blank=True,
        verbose_name='协议类型',
        help_text='协议类型')
    method = models.CharField(
        max_length=10,
        default='GET',
        null=True,
        blank=True,
        choices=METHOD_TPYE,
        verbose_name='请求方法',
        help_text='请求方法')
    # header =  models.ForeignKey(RequestHeaders,null=True, blank=True, verbose_name='接口请求header',
    #                             help_text='接口请求header', on_delete=models.SET_NULL)
    # body = models.ForeignKey(InterfaceParas, null=True, blank=True, verbose_name='请求参数', help_text='请求参数',
    #                              on_delete=models.SET_NULL)
    status = models.SmallIntegerField(
        default=1,
        choices=INTTERFACE_STATUS,
        verbose_name='接口状态',
        null=True,
        blank=True,
        help_text='接口状态')
    sign = models.SmallIntegerField(
        default=0,
        choices=SIGN,
        null=True,
        blank=True,
        verbose_name='接口是否加密',
        help_text='接口是否加密')
    operator = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='操作人',
        help_text='操作人')
    desc = models.CharField(max_length=200, default='', blank=True, null=True,
                            verbose_name='接口描述', help_text='接口描述')
    m_time = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
        help_text='更新时间')
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
        help_text='创建时间')

    class Meta:
        verbose_name = '接口管理'
        verbose_name_plural = verbose_name
        db_table = "api_managerment"

    def __str__(self):
        return self.name


class AllHeaders(models.Model):
    """
    接口请求header
    """
    api = models.ForeignKey(
        ApiManagerment,
        null=True,
        blank=True,
        verbose_name='所属接口',
        related_name="headers",
        on_delete=models.CASCADE)
    name = models.CharField(
        max_length=126,
        default='',
        blank=True,
        verbose_name='请求参数名称')
    value = models.CharField(
        max_length=126,
        default='',
        blank=True,
        help_text='参数值')
    raw = models.TextField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name='raw格式hearer')

    class Meta:
        verbose_name = '接口请求header'
        verbose_name_plural = verbose_name
        db_table = 'api_header'
        unique_together = ('name', 'api')

    def __str__(self):
        return self.name


class ApiParams(models.Model):
    """
    接口请求参数
    """
    api = models.ForeignKey(
        ApiManagerment,
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name='所属接口',
        related_name="paramars")
    name = models.CharField(
        max_length=200,
        default='',
        null=True,
        blank=True,
        verbose_name='参数名称',
        help_text='参数名称')
    value = models.TextField(
        max_length=2048,
        default='',
        null=True,
        blank=True,
        verbose_name='参数值',
        help_text='参数值')
    raw = models.TextField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name='raw格式')

    class Meta:
        verbose_name = '接口请求参数'
        verbose_name_plural = verbose_name
        db_table = 'api_parameters'
        unique_together = ('name', 'api')

    def __str__(self):
        return self.name


class ApiResponse(models.Model):
    """
    单接口返回结果
    """
    RESULT_STATUS = (('success', '成功'),
                     ('danger', '失败'))
    api = models.ForeignKey(
        ApiManagerment,
        null=True,
        blank=True,
        verbose_name='所属接口',
        on_delete=models.CASCADE,
        related_name="response")
    status_code = models.IntegerField(
        null=True, blank=True, verbose_name='状态码')
    response_status = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name='返回状态')
    response_header = models.TextField(
        null=True, blank=True, verbose_name='服务器响应头')
    response_content = models.TextField(
        null=True, blank=True, verbose_name='接口返回数据')
    response_time = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name='接口响应时间')
    create_time = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name='创建时间',
        help_text='创建时间')

    class Meta:
        verbose_name = '接口返回结果'
        verbose_name_plural = verbose_name
        db_table = "api_response"
        ordering = ('-create_time',)

    def __str__(self):
        return self.response_status


def genKeys():
    """
    返回自定义变量key
    :return:
    """
    return str(uuid.uuid4()).replace('-', '').upper()[:10]


class CustomParameters(BaseModel):
    """
    自定义变量
    """
    name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='变量名称')
    key = models.CharField(
        max_length=20,
        null=True,
        blank=False,
        verbose_name='变量key')
    value = models.CharField(
        max_length=126,
        null=True,
        blank=True,
        verbose_name='变量值')
    p_type = models.SmallIntegerField(default=1, verbose_name='变量类型')  # 默认为常量
    max = models.SmallIntegerField(blank=True, null=True, verbose_name='最大值')
    min = models.SmallIntegerField(blank=True, null=True, verbose_name='最小值')
    date_type = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name='日期格式类型')
    str_type = models.SmallIntegerField(
        default=1, blank=True, null=True, verbose_name='字符串格式类型')
    str_length = models.SmallIntegerField(
        blank=True, null=True, verbose_name='字符串长度')
    uuid_type = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name='UUID格式类型')

    class Meta:
        verbose_name = '自定义变量'
        verbose_name_plural = verbose_name
        db_table = "custom_parameters"

    def __str__(self):
        return self.name


class ApiMock(BaseModel):
    """
    接口mock
    """
    # 方法类型
    METHOD_TPYE = (('GET', 'GET'),
                   ('POST', 'POST'),
                   ('DELETE', 'DELETE'),
                   ('PUT', 'PUT'),
                   ('PATCH', 'PATCH'),
                   ('HEAD', 'HEAD'),
                   ('OPTIONS', 'OPTIONS'))
    # 协议类型
    PROTOCOL_TPYE = (('HTTP', 'HTTP'),
                     ('HTTPS', 'HTTPS'))

    INTTERFACE_STATUS = ((1, '可用'),
                         (2, '禁用'))
    # 请求体类型
    body_choice = (
        ("application/x-www-form-urlencoded", "application/x-www-form-urlencoded"),
        ("application/json", "application/json"),
        ("multipart/form-data", "multipart/form-data"),
        ("text/xml", "text/xml"),
    )

    env = models.ForeignKey(
        EnvManager,
        null=True,
        blank=True,
        verbose_name="所属环境",
        help_text="所属环境",
        on_delete=models.SET_NULL)
    name = models.CharField(
        max_length=20,
        default='',
        null=True,
        blank=True,
        verbose_name='接口名称',
        help_text='接口名称')
    url = models.CharField(
        max_length=100,
        default='',
        null=True,
        blank=True,
        verbose_name='接口路径',
        help_text='接口路径')
    protocol = models.CharField(
        max_length=10,
        default='HTTP',
        choices=PROTOCOL_TPYE,
        null=True,
        blank=True,
        verbose_name='协议类型',
        help_text='协议类型')
    method = models.CharField(
        max_length=10,
        default='GET',
        null=True,
        blank=True,
        choices=METHOD_TPYE,
        verbose_name='请求方法',
        help_text='请求方法')
    mock_headers = models.TextField(
        null=True,
        blank=True,
        verbose_name='接口请求header',
        default='',
        help_text='请输入字典格式的请求头')
    mock_param = models.TextField(
        null=True,
        blank=True,
        verbose_name='请求参数',
        help_text='请输入字典格式的请求参数',
        default='')

    body_type = models.CharField(
        choices=body_choice, max_length=21,
        blank=True, null=True,
        verbose_name="请求体类型", default="x-www-form-urlencoded",
        help_text="请选择请求体类型")
    mock_bodys = models.TextField(
        null=True,
        blank=True,
        verbose_name='请求体',
        help_text='请求体',
        default='')

    response_content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Mock接口返回数据',
        default='',
        help_text='请输入字典格式的响应结果')
    status = models.SmallIntegerField(
        default=1,
        choices=INTTERFACE_STATUS,
        verbose_name='接口状态',
        null=True,
        blank=True,
        help_text='接口状态')
    desc = models.CharField(max_length=200, default='', blank=True, null=True,
                            verbose_name='接口描述', help_text='接口描述')
    mock_times = models.SmallIntegerField(
        null=True, blank=True, verbose_name='接口请求次数', default=0)
    delay = models.SmallIntegerField(blank=True, null=True, default=0,
                                     verbose_name='接口延迟执行时间（毫秒）',
                                     help_text='接口延迟执行时间（毫秒）')

    class Meta:
        verbose_name = '接口mock'
        verbose_name_plural = verbose_name
        db_table = 'api_mock'
        unique_together = ('url', 'method')

    def __str__(self):
        return self.name


class CustomFunc(models.Model):
    """
    自定义py函数
    """
    fileName = models.CharField(max_length=20,verbose_name='函数文件名称')
    funName = models.CharField(max_length=124,verbose_name='函数名称')
    content = models.TextField(verbose_name='函数内')
    funcResult = models.CharField(max_length=128,verbose_name='函数返回值')

    class Meta:
        verbose_name = '自定义函数'
        verbose_name_plural = verbose_name
        db_table = 'custom_func'


class CaseGroup(models.Model):
    """
    分组
    """
    name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="分组名称")
    group = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name="上级分组",
        related_name='groups')
    level = models.SmallIntegerField(verbose_name='分组深度', default=1)

    class Meta:
        db_table = 'case_group'

    def __str__(self):
        return self.name


class CaseManagerment(BaseModel):
    """
    用例
    """
    CaseLevel = ((1, '低'),
                 (2, '中'),
                 (3, '高'))
    CaseStatus = ((1, '已废弃'),
                  (2, '待更新'),
                  (3, '正常'))
    CaseType = ((1, '功能测试'), (2, '性能测试'), (3, '安全性测试'), (4, '其他'))

    case_group = models.ForeignKey(
        CaseGroup,
        null=True,
        blank=True,
        related_name='cases',
        on_delete=models.SET_NULL,
        verbose_name='用例所属分组',
        help_text='用例所属分组')
    env = models.ForeignKey(
        EnvManager,
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name='所属环境')
    model = models.ForeignKey(
        ModelManager,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='用例所属模块',
        help_text='用例所属模块')
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='用例名称',
        default='',
        help_text='用例名称')
    caseLevel = models.CharField(
        max_length=126,
        choices=CaseLevel,
        blank=True,
        null=True,
        verbose_name='用例等级',
        help_text='用例等级')
    caseStatus = models.CharField(
        max_length=126,
        choices=CaseStatus,
        blank=True,
        null=True,
        verbose_name='用例状态',
        help_text='用例状态')
    caseType = models.CharField(
        max_length=126,
        choices=CaseType,
        blank=True,
        null=True,
        verbose_name='用例类型',
        help_text='用例类型')
    create_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='创建人',
        help_text='创建人')
    comment = models.TextField(
        default='',
        blank=True,
        null=True,
        verbose_name='评论/描述',
        help_text='评论/描述')
    case_result = models.CharField(
        max_length=126,
        verbose_name='用例结果',
        blank=True,
        null=True)

    class Meta:
        verbose_name = '用例管理'
        verbose_name_plural = verbose_name
        db_table = "cases"

    def __str__(self):
        return self.name


class CaseApi(BaseModel):
    """
    用例接口
    """
    # 方法类型
    METHOD_TPYE = (('GET', 'GET'),
                   ('POST', 'POST'),
                   ('DELETE', 'DELETE'),
                   ('PUT', 'PUT'),
                   ('PATCH', 'PATCH'),
                   ('HEAD', 'HEAD'),
                   ('OPTIONS', 'OPTIONS'))
    # 协议类型
    PROTOCOL_TPYE = (('HTTP', 'HTTP'),
                     ('HTTPS', 'HTTPS'))
    # 接口状态
    INTTERFACE_STATUS = ((1, '可用'),
                         (2, '禁用'))

    id = models.AutoField(db_index=True, primary_key=True, verbose_name='主键')
    case = models.ForeignKey(
        CaseManagerment,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='所属用例',
        related_name='case_api')
    api = models.ForeignKey(
        'self',
        verbose_name='可能关联的api',
        on_delete=models.SET_NULL,
        null=True)
    name = models.CharField(
        max_length=20,
        default='',
        null=True,
        blank=True,
        verbose_name='接口名称',
        help_text='接口名称')
    url = models.CharField(
        max_length=100,
        default='',
        null=True,
        blank=True,
        verbose_name='接口路径',
        help_text='接口路径')
    protocol = models.CharField(
        max_length=10,
        default='HTTP',
        choices=PROTOCOL_TPYE,
        null=True,
        blank=True,
        verbose_name='协议类型',
        help_text='协议类型')
    method = models.CharField(
        max_length=10,
        default='GET',
        null=True,
        blank=True,
        choices=METHOD_TPYE,
        verbose_name='请求方法',
        help_text='请求方法')
    header_is_check = models.BooleanField(
        verbose_name='是否检查header', default=False)
    body_is_check = models.BooleanField(verbose_name='是否检查body', default=False)
    status = models.SmallIntegerField(
        default=1,
        choices=INTTERFACE_STATUS,
        verbose_name='接口状态',
        null=True,
        blank=True,
        help_text='接口状态')
    response_time = models.FloatField(
        null=True, blank=True, verbose_name='接口响应时间')
    count = models.IntegerField(verbose_name='接口执行次数', default=0)
    execution_sequence = models.SmallIntegerField(
        default=0, verbose_name='接口执行顺序')

    class Meta:
        verbose_name = '用例接口'
        verbose_name_plural = verbose_name
        db_table = "case_api"

    def __str__(self):
        return self.name


class CaseApiResponse(models.Model):
    """
    用例接口返回结果
    """
    RESULT_STATUS = (('success', '成功'),
                     ('danger', '失败'))
    case_api = models.ForeignKey(
        CaseApi,
        null=True,
        blank=True,
        verbose_name='所属接口',
        on_delete=models.CASCADE,
        related_name="response_case_api")
    status_code = models.IntegerField(
        null=True, blank=True, verbose_name='状态码')
    response_status = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name='返回状态')
    response_header = models.TextField(
        null=True, blank=True, verbose_name='服务器响应头')
    response_content = models.TextField(
        null=True, blank=True, verbose_name='接口返回数据')
    response_time = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name='接口响应时间')
    create_time = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name='创建时间',
        help_text='创建时间')

    class Meta:
        verbose_name = '用例接口返回结果'
        verbose_name_plural = verbose_name
        db_table = "case_api_response"
        ordering = ('-create_time',)

    def __str__(self):
        return self.response_status


class CheckResult(BaseModel):
    """
    用例检查点
    """

    CHECK_TYPE = ((1, 'Status code'), (2, 'Header'), (3, 'JSON body'),
                  (4, 'Body content'), (5, 'Duration (ms)'))

    case_api = models.ForeignKey(
        CaseApi,
        null=True,
        blank=True,
        verbose_name='所属接口',
        related_name="case_check",
        on_delete=models.CASCADE)
    check_type = models.SmallIntegerField(
        choices=CHECK_TYPE,
        null=True,
        blank=True,
        verbose_name='检查点类型')
    assert_type = models.SmallIntegerField(
        null=True, blank=True, verbose_name='断言方式')
    check_data = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='期望值')
    actual_data = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='实际值')
    check_result = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='检查结果')
    check_jsonpath = models.TextField(default='', null=True, blank=True,
                                      verbose_name='json path')
    check_header_name = models.TextField(default='', null=True, blank=True,
                                         verbose_name='header名称')

    class Meta:
        verbose_name = '用例接口检查点'
        verbose_name_plural = verbose_name
        db_table = 'check_result'

    def __str__(self):
        return self.actual_data


class ExtractResult(BaseModel):
    """
    接口返回数据提取
    """
    case_api = models.ForeignKey(
        CaseApi,
        null=True,
        blank=True,
        verbose_name='所属接口',
        related_name="case_extract",
        on_delete=models.CASCADE)
    extract_type = models.CharField(
        max_length=126,
        null=True,
        blank=True,
        verbose_name='参数提取方式')
    extract_header_name = models.TextField(
        default='', null=True, blank=True, verbose_name='提取header名称')
    extract_jsonpath = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='提取jsonpath路径')
    extract_data = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='提取参数')
    extract_result = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='参数提取值')
    references_field = models.CharField(max_length=128, verbose_name='需要引用的数据')

    class Meta:
        verbose_name = '用例接口数据提取'
        verbose_name_plural = verbose_name
        db_table = 'extract_result'

    def __str__(self):
        return self.extract_result


class CaseReport(models.Model):
    """
    用例报告
    """
    case = models.ForeignKey(
        CaseManagerment,
        null=True,
        blank=True,
        verbose_name='所属接口',
        related_name="case_report",
        on_delete=models.CASCADE)
    total_time = models.CharField(max_length=10, verbose_name='用例运行时间')
    total_cases = models.SmallIntegerField(verbose_name='用例个数')
    success_num = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name='成功个数')
    fail_num = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name='失败个数')
    case_status = models.CharField(
        max_length=126,
        null=True,
        blank=True,
        verbose_name='用例状态')
    case_pass_rate = models.FloatField(verbose_name='测试通过率')
    create_time = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name='创建时间',
        help_text='创建时间')

    class Meta:
        verbose_name = '用例报告'
        verbose_name_plural = verbose_name
        db_table = 'case_report'

    def __str__(self):
        return self.case_pass_rate


class CaseStepHeaders(BaseModel):
    """
    接口请求header
    """
    case_api = models.ForeignKey(
        CaseApi,
        null=True,
        blank=True,
        verbose_name='所属接口',
        related_name="case_headers",
        on_delete=models.CASCADE)
    name = models.CharField(
        max_length=126,
        default='',
        blank=True,
        verbose_name='请求参数名称')
    value = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        help_text='参数值')

    class Meta:
        verbose_name = '用例接口请求header'
        verbose_name_plural = verbose_name
        db_table = 'case_step_header'
        unique_together = ('name', 'case_api')

    def __str__(self):
        return self.name


class CaseStepParams(BaseModel):
    """
    接口请求参数
    """

    case_api = models.ForeignKey(
        CaseApi,
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name='所属接口',
        related_name="case_paramars")
    name = models.CharField(
        max_length=200,
        default='',
        null=True,
        blank=True,
        verbose_name='参数名称',
        help_text='参数名称')
    value = models.TextField(
        max_length=2048,
        default='',
        null=True,
        blank=True,
        verbose_name='参数值',
        help_text='参数值')
    raw = models.TextField(
        max_length=2048,
        default='',
        blank=True,
        verbose_name='raw格式')

    class Meta:
        verbose_name = '用例接口请求参数'
        verbose_name_plural = verbose_name
        db_table = 'case_step_parameters'
        unique_together = ('name', 'case_api')

    def __str__(self):
        return self.name
