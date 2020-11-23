# Generated by Django 2.2.17 on 2020-11-12 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0010_auto_20200513_1501'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiManagerment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', help_text='接口名称', max_length=20, null=True, verbose_name='接口名称')),
                ('url', models.CharField(blank=True, default='', help_text='接口路径', max_length=100, null=True, verbose_name='接口路径')),
                ('protocol', models.CharField(blank=True, choices=[('HTTP', 'HTTP'), ('HTTPS', 'HTTPS')], default='HTTP', help_text='协议类型', max_length=10, null=True, verbose_name='协议类型')),
                ('method', models.CharField(blank=True, choices=[('GET', 'GET'), ('POST', 'POST'), ('DELETE', 'DELETE'), ('PUT', 'PUT'), ('PATCH', 'PATCH'), ('HEAD', 'HEAD'), ('OPTIONS', 'OPTIONS')], default='GET', help_text='请求方法', max_length=10, null=True, verbose_name='请求方法')),
                ('status', models.SmallIntegerField(blank=True, choices=[(1, '可用'), (2, '禁用')], default=1, help_text='接口状态', null=True, verbose_name='接口状态')),
                ('sign', models.SmallIntegerField(blank=True, choices=[(1, '不加密'), (2, '加密')], default=0, help_text='接口是否加密', null=True, verbose_name='接口是否加密')),
                ('desc', models.CharField(blank=True, default='', help_text='接口描述', max_length=200, null=True, verbose_name='接口描述')),
                ('m_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('env', models.ForeignKey(blank=True, help_text='所属环境', null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.EnvManager', verbose_name='所属环境')),
                ('model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.ModelManager', verbose_name='模块名称')),
                ('operator', models.ForeignKey(blank=True, help_text='操作人', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='操作人')),
            ],
            options={
                'verbose_name': '接口管理',
                'verbose_name_plural': '接口管理',
                'db_table': 'api_managerment',
            },
        ),
        migrations.CreateModel(
            name='CaseApi',
            fields=[
                ('m_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False, verbose_name='主键')),
                ('name', models.CharField(blank=True, default='', help_text='接口名称', max_length=20, null=True, verbose_name='接口名称')),
                ('url', models.CharField(blank=True, default='', help_text='接口路径', max_length=100, null=True, verbose_name='接口路径')),
                ('protocol', models.CharField(blank=True, choices=[('HTTP', 'HTTP'), ('HTTPS', 'HTTPS')], default='HTTP', help_text='协议类型', max_length=10, null=True, verbose_name='协议类型')),
                ('method', models.CharField(blank=True, choices=[('GET', 'GET'), ('POST', 'POST'), ('DELETE', 'DELETE'), ('PUT', 'PUT'), ('PATCH', 'PATCH'), ('HEAD', 'HEAD'), ('OPTIONS', 'OPTIONS')], default='GET', help_text='请求方法', max_length=10, null=True, verbose_name='请求方法')),
                ('header_is_check', models.BooleanField(default=False, verbose_name='是否检查header')),
                ('body_is_check', models.BooleanField(default=False, verbose_name='是否检查body')),
                ('status', models.SmallIntegerField(blank=True, choices=[(1, '可用'), (2, '禁用')], default=1, help_text='接口状态', null=True, verbose_name='接口状态')),
                ('response_time', models.FloatField(blank=True, null=True, verbose_name='接口响应时间')),
                ('count', models.IntegerField(default=0, verbose_name='接口执行次数')),
                ('api', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cases.CaseApi', verbose_name='可能关联的api')),
            ],
            options={
                'verbose_name': '用例接口',
                'verbose_name_plural': '用例接口',
                'db_table': 'case_api',
            },
        ),
        migrations.CreateModel(
            name='CaseGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='分组名称')),
                ('level', models.SmallIntegerField(default=1, verbose_name='分组深度')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='cases.CaseGroup', verbose_name='上级分组')),
            ],
            options={
                'db_table': 'case_group',
            },
        ),
        migrations.CreateModel(
            name='CaseManagerment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('name', models.CharField(blank=True, default='', help_text='用例名称', max_length=255, null=True, verbose_name='用例名称')),
                ('caseLevel', models.CharField(blank=True, choices=[(1, '低'), (2, '中'), (3, '高')], help_text='用例等级', max_length=126, null=True, verbose_name='用例等级')),
                ('caseStatus', models.CharField(blank=True, choices=[(1, '已废弃'), (2, '待更新'), (3, '正常')], help_text='用例状态', max_length=126, null=True, verbose_name='用例状态')),
                ('caseType', models.CharField(blank=True, choices=[(1, '功能测试'), (2, '性能测试'), (3, '安全性测试'), (4, '其他')], help_text='用例类型', max_length=126, null=True, verbose_name='用例类型')),
                ('comment', models.TextField(blank=True, default='', help_text='评论/描述', null=True, verbose_name='评论/描述')),
                ('case_result', models.CharField(blank=True, max_length=126, null=True, verbose_name='用例结果')),
                ('case_group', models.ForeignKey(blank=True, help_text='用例所属分组', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cases', to='cases.CaseGroup', verbose_name='用例所属分组')),
                ('create_user', models.ForeignKey(blank=True, help_text='创建人', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('env', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.EnvManager', verbose_name='所属环境')),
                ('model', models.ForeignKey(blank=True, help_text='用例所属模块', null=True, on_delete=django.db.models.deletion.CASCADE, to='base.ModelManager', verbose_name='用例所属模块')),
            ],
            options={
                'verbose_name': '用例管理',
                'verbose_name_plural': '用例管理',
                'db_table': 'cases',
            },
        ),
        migrations.CreateModel(
            name='CustomParameters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='变量名称')),
                ('key', models.CharField(max_length=20, null=True, verbose_name='变量key')),
                ('value', models.CharField(blank=True, max_length=126, null=True, verbose_name='变量值')),
                ('p_type', models.SmallIntegerField(default=1, verbose_name='变量类型')),
                ('max', models.SmallIntegerField(blank=True, null=True, verbose_name='最大值')),
                ('min', models.SmallIntegerField(blank=True, null=True, verbose_name='最小值')),
                ('date_type', models.CharField(blank=True, max_length=30, null=True, verbose_name='日期格式类型')),
                ('str_type', models.SmallIntegerField(blank=True, default=1, null=True, verbose_name='字符串格式类型')),
                ('str_length', models.SmallIntegerField(blank=True, null=True, verbose_name='字符串长度')),
                ('uuid_type', models.CharField(blank=True, max_length=300, null=True, verbose_name='UUID格式类型')),
            ],
            options={
                'verbose_name': '自定义变量',
                'verbose_name_plural': '自定义变量',
                'db_table': 'custom_parameters',
            },
        ),
        migrations.CreateModel(
            name='Headers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('name', models.CharField(default='', max_length=124, verbose_name='Header名称')),
                ('value', models.CharField(default='', max_length=124, verbose_name='Header值')),
                ('add_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='添加人')),
            ],
            options={
                'verbose_name': '接口模板',
                'verbose_name_plural': '接口模板',
                'db_table': 'header_template',
            },
        ),
        migrations.CreateModel(
            name='ExtractResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('extract_type', models.CharField(blank=True, max_length=126, null=True, verbose_name='参数提取方式')),
                ('extract_header_name', models.TextField(blank=True, default='', null=True, verbose_name='提取header名称')),
                ('extract_jsonpath', models.TextField(blank=True, default='', null=True, verbose_name='提取jsonpath路径')),
                ('extract_data', models.TextField(blank=True, default='', null=True, verbose_name='提取参数')),
                ('extract_result', models.TextField(blank=True, default='', null=True, verbose_name='参数提取值')),
                ('references_field', models.CharField(max_length=128, verbose_name='需要引用的数据')),
                ('case_api', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='case_extract', to='cases.CaseApi', verbose_name='所属接口')),
            ],
            options={
                'verbose_name': '用例接口数据提取',
                'verbose_name_plural': '用例接口数据提取',
                'db_table': 'extract_result',
            },
        ),
        migrations.CreateModel(
            name='CheckResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('check_type', models.SmallIntegerField(blank=True, choices=[(1, 'Status code'), (2, 'Header'), (3, 'JSON body'), (4, 'Body content'), (5, 'Duration (ms)')], null=True, verbose_name='检查点类型')),
                ('assert_type', models.SmallIntegerField(blank=True, null=True, verbose_name='断言方式')),
                ('check_data', models.TextField(blank=True, default='', null=True, verbose_name='期望值')),
                ('actual_data', models.TextField(blank=True, default='', null=True, verbose_name='实际值')),
                ('check_result', models.TextField(blank=True, default='', null=True, verbose_name='检查结果')),
                ('check_jsonpath', models.TextField(blank=True, default='', null=True, verbose_name='json path')),
                ('check_header_name', models.TextField(blank=True, default='', null=True, verbose_name='header名称')),
                ('case_api', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='case_check', to='cases.CaseApi', verbose_name='所属接口')),
            ],
            options={
                'verbose_name': '用例接口检查点',
                'verbose_name_plural': '用例接口检查点',
                'db_table': 'check_result',
            },
        ),
        migrations.CreateModel(
            name='CaseReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_time', models.CharField(max_length=10, verbose_name='用例运行时间')),
                ('total_cases', models.SmallIntegerField(verbose_name='用例个数')),
                ('success_num', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='成功个数')),
                ('fail_num', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='失败个数')),
                ('case_status', models.CharField(blank=True, max_length=126, null=True, verbose_name='用例状态')),
                ('case_pass_rate', models.FloatField(verbose_name='测试通过率')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='case_report', to='cases.CaseManagerment', verbose_name='所属接口')),
            ],
            options={
                'verbose_name': '用例报告',
                'verbose_name_plural': '用例报告',
                'db_table': 'case_report',
            },
        ),
        migrations.CreateModel(
            name='CaseApiResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.IntegerField(blank=True, null=True, verbose_name='状态码')),
                ('response_status', models.CharField(blank=True, max_length=10, null=True, verbose_name='返回状态')),
                ('response_header', models.TextField(blank=True, null=True, verbose_name='服务器响应头')),
                ('response_content', models.TextField(blank=True, null=True, verbose_name='接口返回数据')),
                ('response_time', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='接口响应时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('case_api', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='response_case_api', to='cases.CaseApi', verbose_name='所属接口')),
            ],
            options={
                'verbose_name': '用例接口返回结果',
                'verbose_name_plural': '用例接口返回结果',
                'db_table': 'case_api_response',
                'ordering': ('-create_time',),
            },
        ),
        migrations.AddField(
            model_name='caseapi',
            name='case',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='case_api', to='cases.CaseManagerment', verbose_name='所属用例'),
        ),
        migrations.CreateModel(
            name='ApiResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.IntegerField(blank=True, null=True, verbose_name='状态码')),
                ('response_status', models.CharField(blank=True, max_length=10, null=True, verbose_name='返回状态')),
                ('response_header', models.TextField(blank=True, null=True, verbose_name='服务器响应头')),
                ('response_content', models.TextField(blank=True, null=True, verbose_name='接口返回数据')),
                ('response_time', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='接口响应时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True, verbose_name='创建时间')),
                ('api', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='response', to='cases.ApiManagerment', verbose_name='所属接口')),
            ],
            options={
                'verbose_name': '接口返回结果',
                'verbose_name_plural': '接口返回结果',
                'db_table': 'api_response',
                'ordering': ('-create_time',),
            },
        ),
        migrations.CreateModel(
            name='CaseStepParams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('name', models.CharField(blank=True, default='', help_text='参数名称', max_length=200, null=True, verbose_name='参数名称')),
                ('value', models.TextField(blank=True, default='', help_text='参数值', max_length=2048, null=True, verbose_name='参数值')),
                ('raw', models.TextField(blank=True, default='', max_length=2048, verbose_name='raw格式')),
                ('case_api', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='case_paramars', to='cases.CaseApi', verbose_name='所属接口')),
            ],
            options={
                'verbose_name': '用例接口请求参数',
                'verbose_name_plural': '用例接口请求参数',
                'db_table': 'case_step_parameters',
                'unique_together': {('name', 'case_api')},
            },
        ),
        migrations.CreateModel(
            name='CaseStepHeaders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('name', models.CharField(blank=True, default='', max_length=126, verbose_name='请求参数名称')),
                ('value', models.CharField(blank=True, default='', help_text='参数值', max_length=1024)),
                ('case_api', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='case_headers', to='cases.CaseApi', verbose_name='所属接口')),
            ],
            options={
                'verbose_name': '用例接口请求header',
                'verbose_name_plural': '用例接口请求header',
                'db_table': 'case_step_header',
                'unique_together': {('name', 'case_api')},
            },
        ),
        migrations.CreateModel(
            name='ApiParams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', help_text='参数名称', max_length=200, null=True, verbose_name='参数名称')),
                ('value', models.TextField(blank=True, default='', help_text='参数值', max_length=2048, null=True, verbose_name='参数值')),
                ('raw', models.TextField(blank=True, default='', max_length=1024, verbose_name='raw格式')),
                ('api', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paramars', to='cases.ApiManagerment', verbose_name='所属接口')),
            ],
            options={
                'verbose_name': '接口请求参数',
                'verbose_name_plural': '接口请求参数',
                'db_table': 'api_parameters',
                'unique_together': {('name', 'api')},
            },
        ),
        migrations.CreateModel(
            name='ApiMock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('name', models.CharField(blank=True, default='', help_text='接口名称', max_length=20, null=True, verbose_name='接口名称')),
                ('url', models.CharField(blank=True, default='', help_text='接口路径', max_length=100, null=True, verbose_name='接口路径')),
                ('protocol', models.CharField(blank=True, choices=[('HTTP', 'HTTP'), ('HTTPS', 'HTTPS')], default='HTTP', help_text='协议类型', max_length=10, null=True, verbose_name='协议类型')),
                ('method', models.CharField(blank=True, choices=[('GET', 'GET'), ('POST', 'POST'), ('DELETE', 'DELETE'), ('PUT', 'PUT'), ('PATCH', 'PATCH'), ('HEAD', 'HEAD'), ('OPTIONS', 'OPTIONS')], default='GET', help_text='请求方法', max_length=10, null=True, verbose_name='请求方法')),
                ('mock_headers', models.TextField(blank=True, default='', help_text='请输入字典格式的请求头', null=True, verbose_name='接口请求header')),
                ('mock_param', models.TextField(blank=True, default='', help_text='请输入字典格式的请求参数', null=True, verbose_name='请求参数')),
                ('body_type', models.CharField(blank=True, choices=[('application/x-www-form-urlencoded', 'application/x-www-form-urlencoded'), ('application/json', 'application/json'), ('multipart/form-data', 'multipart/form-data'), ('text/xml', 'text/xml')], default='x-www-form-urlencoded', help_text='请选择请求体类型', max_length=21, null=True, verbose_name='请求体类型')),
                ('mock_bodys', models.TextField(blank=True, default='', help_text='请求体', null=True, verbose_name='请求体')),
                ('response_content', models.TextField(blank=True, default='', help_text='请输入字典格式的响应结果', null=True, verbose_name='Mock接口返回数据')),
                ('status', models.SmallIntegerField(blank=True, choices=[(1, '可用'), (2, '禁用')], default=1, help_text='接口状态', null=True, verbose_name='接口状态')),
                ('desc', models.CharField(blank=True, default='', help_text='接口描述', max_length=200, null=True, verbose_name='接口描述')),
                ('mock_times', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='接口请求次数')),
                ('delay', models.SmallIntegerField(blank=True, default=0, help_text='接口延迟执行时间（毫秒）', null=True, verbose_name='接口延迟执行时间（毫秒）')),
                ('env', models.ForeignKey(blank=True, help_text='所属环境', null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.EnvManager', verbose_name='所属环境')),
            ],
            options={
                'verbose_name': '接口mock',
                'verbose_name_plural': '接口mock',
                'db_table': 'api_mock',
                'unique_together': {('url', 'method')},
            },
        ),
        migrations.CreateModel(
            name='AllHeaders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=126, verbose_name='请求参数名称')),
                ('value', models.CharField(blank=True, default='', help_text='参数值', max_length=126)),
                ('raw', models.TextField(blank=True, default='', max_length=1024, verbose_name='raw格式hearer')),
                ('api', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='headers', to='cases.ApiManagerment', verbose_name='所属接口')),
            ],
            options={
                'verbose_name': '接口请求header',
                'verbose_name_plural': '接口请求header',
                'db_table': 'api_header',
                'unique_together': {('name', 'api')},
            },
        ),
    ]
