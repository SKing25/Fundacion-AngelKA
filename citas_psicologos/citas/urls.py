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

    # Ruta para la vista de registro
    path('register/', views.registro_view, name='registro'),

    # Ruta para mostrar la interfaz del psicólogo
    path('psicologo/', views.mostrar_interfaz_psicologo, name='interfaz_psicologo'),

    # Ruta para mostrar la interfaz del paciente
    path('paciente/', views.mostrar_interfaz_paciente, name='interfaz_paciente'),

    # Ruta para la vista del superusuario
    path('superusuario/', views.vista_superusuario, name='vista_superusuario'),

    # Ruta para ver el calendario de citas
    path('calendario/', views.calendario_citas, name='calendario_citas'),

    # Ruta para cerrar sesión
    path('logout/', views.vista_logout, name='vista_logout'),

    # Ruta para la página "Soy Psicólogo"
    path('soy_psicologo/', views.soy_psicologo, name='soy_psicologo'),

    # Ruta para restablecer la contraseña de un usuario específico
    path('restablecer_contraseña/<int:user_id>/', views.restablecer_contraseña, name='restablecer_contraseña'),

    # Ruta para descargar citas en formato PDF
    path('descargar_citas_pdf/', views.descargar_citas_pdf, name='descargar_citas_pdf'),

    # Ruta para descargar todas las citas en formato PDF
    path('descargar_todas_citas_pdf/', views.descargar_todas_citas_pdf, name='descargar_todas_citas_pdf'),
]
