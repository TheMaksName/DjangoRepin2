# reg/apps.py
from django.apps import AppConfig

class RegConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reg'  # Используем только имя приложения без префиксов

    def ready(self):
        # Импортируем сигналы после загрузки приложения
        from . import signals  # Точка означает текущий каталог (reg)