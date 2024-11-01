# Este archivo configura el servidor WSGI (Web Server Gateway Interface) para tu proyecto Django, 
# permitiendo que sea servido por servidores web compatibles con WSGI.

"""
WSGI config for citas_psicologos project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Establecer la configuración predeterminada para el proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'citas_psicologos.settings')

# Obtener la aplicación WSGI
application = get_wsgi_application()
