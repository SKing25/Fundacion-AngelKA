# Este archivo configura el servidor ASGI (Asynchronous Server Gateway Interface) para tu proyecto Django, permitiendo manejar solicitudes asíncronas.

"""
ASGI config for citas_psicologos project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Establecer la configuración predeterminada para el proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citas_psicologos.settings')

# Obtener la aplicación ASGI
application = get_asgi_application()
