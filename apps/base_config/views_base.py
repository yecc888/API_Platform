__author__ = 'yecc'
__date__ = '2019/11/29 14:55'

from django.views.generic.base import View
from .models import EnvManager


class envsListView(View):
    def get(self, request):
        json_list = []
        envs = EnvManager.objects.all()
        # for env in envs:
        #     env_dict = {}
        #     env_dict['env_name'] = env.env_name
        #     env_dict['env_desc'] = env.env_desc
        #     env_dict['env_type'] = env.env_type
        #     env_dict['host'] = env.host
        #     env_dict['port'] = env.port
        #     env_dict['env_status'] = env.env_status
        #     env_dict['enc_info'] = env.env_info
        #     # env_dict['create_time'] = env.create_time
        #     json_list.append(env_dict)
        # from django.forms.models import model_to_dict
        # for env in envs:
        #     json_dict = model_to_dict(env)
        #     json_list.append(json_dict)
        from django.core.serializers import serialize
        import json
        json_data = serialize('json',envs)
        types = type(json_data)
        json_data = json.loads(json_data)
        # 返回json数据
        from django.http import HttpResponse,JsonResponse
        # return HttpResponse(json.dumps(json_list), content_type="application/json")
        return JsonResponse(json_data, safe=False)



