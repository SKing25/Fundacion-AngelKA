# Este archivo contiene la lógica de presentación de tu aplicación. 
# Aquí defines las funciones que responden a las solicitudes HTTP y renderizan las plantillas.

# views.py
# Elimina todas las referencias a 'SuperUsuario'

# views.py
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Psicologo, Cita
from .forms import FormularioLogin, FormularioRegistro
from datetime import date
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import CitaForm
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# views.py
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Cita
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def descargar_todas_citas_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=todas_citas.pdf'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.drawString(100, height - 50, "Todas las Citas de Psicólogos")

    citas = Cita.objects.all()

    y = height - 100
    for cita in citas:
        p.drawString(100, y, f"Psicólogo: {cita.psicologo.nombre} - Fecha: {cita.fecha} - Hora: {cita.hora} - Paciente: {cita.paciente}")
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()
    return response


@login_required(login_url='vista_login')
def descargar_citas_pdf(request):
    # Crear el objeto HttpResponse con el header de descarga
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=citas_pendientes.pdf'

    # Crear el objeto PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Título del PDF
    p.drawString(100, height - 50, f"Citas Pendientes de {request.user.nombre}")

    # Obtener las citas pendientes del psicólogo
    citas = Cita.objects.filter(psicologo=request.user)

    # Añadir las citas al PDF
    y = height - 100
    for cita in citas:
        p.drawString(100, y, f"Fecha: {cita.fecha} - Hora: {cita.hora} - Paciente: {cita.paciente}")
        y -= 20

    # Finalizar el PDF
    p.showPage()
    p.save()
    return response


@login_required(login_url='vista_login')
def mostrar_interfaz_psicologo(request):
    citas = Cita.objects.filter(psicologo=request.user)
    if request.method == 'POST':
        cita_id = request.POST.get('cita_id')
        cita = Cita.objects.get(id=cita_id)
        # Eliminar la cita cuando se marca como completa
        cita.delete()
        return redirect('interfaz_psicologo')

    context = {
        'user': request.user,
        'citas': citas,
    }
    return render(request, 'interfaz_psicologo.html', context)

# Vista para mostrar el menú principal
def mostrar_menu_principal(request):
    return render(request, 'menu_principal.html')

# Vista de login para psicólogos y superusuarios
def vista_login(request):
    mensaje_error = None
    if request.method == 'POST':
        formulario = FormularioLogin(request.POST)
        if formulario.is_valid():
            correo = formulario.cleaned_data['correo']
            contraseña = formulario.cleaned_data['contraseña']
            usuario = authenticate(request, correo=correo, password=contraseña)  # Cambio aquí
            if usuario is not None:
                login(request, usuario)
                if usuario.is_superuser:
                    return redirect('vista_superusuario')
                else:
                    return redirect('interfaz_psicologo')
            else:
                mensaje_error = "Correo o contraseña incorrectos."
    else:
        formulario = FormularioLogin()
    return render(request, 'login.html', {'formulario': formulario, 'mensaje_error': mensaje_error})

# Vista de registro
def registro_view(request):
    if request.method == 'POST':
        formulario = FormularioRegistro(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('vista_login')
    else:
        formulario = FormularioRegistro()
    return render(request, 'registro.html', {'formulario': formulario})

# Vista para la interfaz del paciente

# views.py
def mostrar_interfaz_paciente(request):
    psicologos = Psicologo.objects.filter(es_psicologo=True)
    mensaje_error = None
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        paciente = request.POST.get('paciente')

        # Filtrar psicólogos disponibles para la fecha y hora especificadas
        psicologos_disponibles = [psicologo for psicologo in psicologos if not Cita.objects.filter(psicologo=psicologo, fecha=fecha, hora=hora).exists()]
        
        if psicologos_disponibles:
            # Seleccionar un psicólogo disponible aleatoriamente
            psicologo_asignado = random.choice(psicologos_disponibles)
            Cita.objects.create(psicologo=psicologo_asignado, fecha=fecha, hora=hora, paciente=paciente)
            return redirect('interfaz_paciente')
        else:
            mensaje_error = "No hay psicólogos disponibles para la fecha y hora seleccionadas."

    return render(request, 'interfaz_paciente.html', {'mensaje_error': mensaje_error})


# Vista para la interfaz del superusuario
def vista_superusuario(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('vista_login')
    psicologos = Psicologo.objects.all()
    return render(request, 'vista_superusuario.html', {'psicologos': psicologos})

# Vista para mostrar el calendario de citas
def calendario_citas(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('vista_login')
    citas = Cita.objects.all().order_by('fecha', 'hora', 'psicologo__nombre')
    return render(request, 'calendario_citas.html', {'citas': citas})

# Vista para descargar el calendario de citas en un archivo Excel
def descargar_calendario_excel(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('vista_login')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="calendario_citas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Hora', 'Psicologo', 'Paciente'])

    citas = Cita.objects.all().order_by('fecha', 'hora', 'psicologo__nombre')
    for cita in citas:
        writer.writerow([cita.fecha, cita.hora, cita.psicologo.nombre, cita.paciente])

    return response

def vista_logout(request):
    logout(request)
    return redirect('menu_principal')


def soy_psicologo(request):
    if request.user.is_authenticated:
        return redirect('interfaz_psicologo')
    else:
        return redirect('vista_login')


def restablecer_contraseña(request, user_id):
    if request.method == 'POST':
        nueva_contraseña = request.POST.get('nueva_contraseña')
        usuario = User.objects.get(id=user_id)
        usuario.password = make_password(nueva_contraseña)
        usuario.save()
        return redirect('admin:index')
    return render(request, 'restablecer_contraseña.html', {'user_id': user_id})