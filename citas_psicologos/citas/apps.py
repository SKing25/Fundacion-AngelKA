# El archivo apps.py en una aplicación de Django se utiliza para configurar algunas de las opciones de la aplicación. 
# Este archivo contiene una clase de configuración de la aplicación que permite especificar ciertos atributos y comportamientos de la aplicación.

from django.apps import AppConfig

# Definir la clase de configuración para la aplicación 'Citas'
class CitasConfig(AppConfig):
    # Establecer el tipo de campo auto incremental por defecto para los modelos de la aplicación
    default_auto_field = 'django.db.models.BigAutoField'
    # Definir el nombre de la aplicación
    name = 'citas'
