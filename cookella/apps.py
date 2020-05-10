from django.apps import AppConfig


class CookellaConfig(AppConfig):
    name = 'cookella'

    def ready(self):
        from . import signals
