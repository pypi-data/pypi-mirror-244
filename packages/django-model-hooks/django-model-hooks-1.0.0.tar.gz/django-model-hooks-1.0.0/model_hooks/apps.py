from django.apps import AppConfig


class ModelHookConfig(AppConfig):
    name = 'model_hooks'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import model_hooks.receivers
