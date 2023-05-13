from django.apps import AppConfig


class CoderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Coder'

    def ready(self):
        import Coder.signals