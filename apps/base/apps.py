from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = 'base'
    verbose_name = '基础配置'

    def ready(self):
        import base.signals


