#Este archivo define las rutas URL de tu aplicación y enlaza cada URL con una vista correspondiente.

from django.urls import path
from . import views

# Definición de rutas URL para la aplicación 'citas'
urlpatterns = [
    path('', views.mostrar_menu_principal, name='menu_principal'),
    path('login/', views.vista_login, name='vista_login'),
    path('register/', views.registro_view, name='registro'),
    path('psicologo/', views.mostrar_interfaz_psicologo, name='interfaz_psicologo'),
    path('paciente/', views.mostrar_interfaz_paciente, name='interfaz_paciente'),
    path('superusuario/', views.vista_superusuario, name='vista_superusuario'),
    path('calendario/', views.calendario_citas, name='calendario_citas'),
    path('descargar_calendario/', views.descargar_calendario_excel, name='descargar_calendario_excel'),
    path('logout/', views.vista_logout, name='vista_logout'),  # Nueva ruta de logout
    path('soy_psicologo/', views.soy_psicologo, name='soy_psicologo'),
    path('restablecer_contraseña/<int:user_id>/', views.restablecer_contraseña, name='restablecer_contraseña'),
    path('descargar_citas_pdf/', views.descargar_citas_pdf, name='descargar_citas_pdf'),
    path('admin/citas/descargar_todas_citas_pdf/', views.descargar_todas_citas_pdf, name='descargar_todas_citas_pdf'),   
]
