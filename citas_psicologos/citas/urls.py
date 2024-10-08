from django.urls import path
from . import views

urlpatterns = [
    path('', views.mostrar_menu_principal, name='menu_principal'),
    path('psicologo/', views.mostrar_interfaz_psicologo, name='interfaz_psicologo'),
    path('paciente/', views.mostrar_interfaz_paciente, name='interfaz_paciente'),
]
