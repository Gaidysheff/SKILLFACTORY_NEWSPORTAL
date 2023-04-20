from django.apps import AppConfig


class NewsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsapp'
    verbose_name = 'newsapp - Новостной портал'

    def ready(self):
        import newsapp.signals
