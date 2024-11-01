# Este archivo define la configuración de la aplicación, incluyendo el nombre de la app y el tipo de clave primaria por defecto.

from django.apps import AppConfig

# Configuración de la aplicación 'citas'
class CitasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'citas'
