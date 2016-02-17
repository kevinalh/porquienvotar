#@PydevCodeAnalysisIgnore
from django.apps import AppConfig


class CodificacionConfig(AppConfig):
    name = 'codificacion'

    def ready(self):
        import codificacion.signals.handlers
