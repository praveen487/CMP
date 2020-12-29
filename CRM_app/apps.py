from django.apps import AppConfig


class CrmAppConfig(AppConfig):
    name = 'CRM_app'

    def ready(self):
        import CRM_app.signals
