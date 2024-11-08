# El archivo urls.py define las rutas URL para la aplicación Django, mapeando las URL a las vistas correspondientes. 
# Esto permite que cada URL en el proyecto llame a la vista correcta que maneja la solicitud.

from django.urls import path
from . import views

# Definir los patrones de URL para la aplicación
urlpatterns = [
    # Ruta para la vista principal del menú
    path('', views.mostrar_menu_principal, name='menu_principal'),

    # Ruta para la vista de inicio de sesión
    path('login/', views.vista_login, name='vista_login'),

    # Ruta para mostrar la interfaz del psicólogo
    path('psicologo/', views.mostrar_interfaz_psicologo, name='interfaz_psicologo'),

    path('marcar_cita_completa/<int:cita_id>/', views.marcar_cita_completa, name='marcar_cita_completa'),

    # Ruta para mostrar la interfaz del paciente
    path('paciente/', views.mostrar_interfaz_paciente, name='interfaz_paciente'),

    # Ruta para cerrar sesión
    path('logout/', views.vista_logout, name='vista_logout'),

    # Ruta para la página "Soy Psicólogo"
    path('soy_psicologo/', views.soy_psicologo, name='soy_psicologo'),

    # Ruta para descargar citas en formato PDF
    path('descargar_citas_pdf/', views.descargar_citas_pdf, name='descargar_citas_pdf'),

    # Ruta para descargar todas las citas en formato PDF
    path('descargar_todas_citas_pdf/', views.descargar_todas_citas_pdf, name='descargar_todas_citas_pdf'),

    path('consultar_cita/', views.consultar_cita, name='consultar_cita'),

    path('modificar_cita/<int:cita_id>/', views.modificar_cita, name='modificar_cita'),

    path('eliminar_cita/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),

    path('editar_perfil_psicologo/', views.editar_perfil_psicologo, name='editar_perfil_psicologo'),
]
