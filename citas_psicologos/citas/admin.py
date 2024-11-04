# El archivo admin.py se utiliza para personalizar el panel de administración de Django. 
# Específicamente, registra los modelos Psicologo y Cita para que puedan ser gestionados desde la interfaz administrativa, 
# y añade funcionalidades personalizadas como la descarga de citas en PDF.

from django.contrib import admin
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from .models import Psicologo, Cita

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Registrar el modelo Psicologo en el panel de administración
@admin.register(Psicologo)
class PsicologoAdmin(admin.ModelAdmin):
    # Especificar los campos que se mostrarán en la lista de registros del panel de administración
    list_display = ('nombre', 'correo', 'contraseña')

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Registrar el modelo Cita en el panel de administración
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    # Especificar los campos que se mostrarán en la lista de registros del panel de administración
    list_display = ('psicologo', 'fecha', 'hora', 'paciente')
    # Añadir filtros para la lista de registros del panel de administración
    list_filter = ('fecha', 'psicologo')
    # Especificar una plantilla personalizada para la vista de lista de cambios
    change_list_template = "admin/citas_change_list.html"

    # Definir URLs personalizadas para el modelo Cita
    def get_urls(self):
        # Obtener las URLs por defecto
        urls = super().get_urls()
        # Añadir una URL personalizada para descargar citas
        custom_urls = [
            path('descargar_citas/', self.admin_site.admin_view(self.descargar_citas), name='descargar_citas'),
        ]
        # Devolver la lista combinada de URLs por defecto y personalizadas
        return custom_urls + urls

    # Definir la vista para la URL personalizada
    def descargar_citas(self, request):
        # Redirigir a la vista de descarga de todas las citas en PDF
        return HttpResponseRedirect(reverse('descargar_todas_citas_pdf'))

#-----------------------------------------------------------------------------------------------------------------------------------------------