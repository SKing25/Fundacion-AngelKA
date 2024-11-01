# admin.py
from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Psicologo, Cita

@admin.register(Psicologo)
class PsicologoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'contraseña')

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('psicologo', 'fecha', 'hora', 'paciente')
    list_filter = ('fecha', 'psicologo')
    change_list_template = "admin/citas_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('descargar_citas/', self.admin_site.admin_view(self.descargar_citas), name='descargar_citas'),
        ]
        return custom_urls + urls

    def descargar_citas(self, request):
        return HttpResponseRedirect(reverse('descargar_todas_citas_pdf'))
