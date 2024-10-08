from django.shortcuts import render, redirect
from .models import Psicologo, Cita
from datetime import date

def mostrar_menu_principal(request):
    return render(request, 'menu_principal.html')

def mostrar_interfaz_psicologo(request):
    psicologos = Psicologo.objects.all()
    citas = []
    psicologo_seleccionado = None
    if 'psicologo' in request.GET:
        psicologo_id = request.GET.get('psicologo')
        psicologo_seleccionado = Psicologo.objects.get(id=psicologo_id)
        citas = Cita.objects.filter(psicologo=psicologo_seleccionado).order_by('fecha', 'hora')
    return render(request, 'interfaz_psicologo.html', {'psicologos': psicologos, 'citas': citas, 'psicologo_seleccionado': psicologo_seleccionado})

def mostrar_interfaz_paciente(request):
    psicologos = Psicologo.objects.all()
    error_message = None
    if request.method == 'POST':
        psicologo_id = request.POST.get('psicologo')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        paciente = request.POST.get('paciente')
        psicologo = Psicologo.objects.get(id=psicologo_id)
        if Cita.objects.filter(psicologo=psicologo, fecha=fecha, hora=hora).exists():
            error_message = "El psicólogo ya tiene una cita en esa fecha y hora."
        else:
            Cita.objects.create(psicologo=psicologo, fecha=fecha, hora=hora, paciente=paciente)
            return redirect('interfaz_paciente')
    return render(request, 'interfaz_paciente.html', {'psicologos': psicologos, 'error_message': error_message})
