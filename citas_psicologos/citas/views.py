# El archivo views.py define las funciones de vista para la aplicación Django. 
# Cada función de vista se encarga de recibir una solicitud HTTP, procesar los datos necesarios y devolver una respuesta HTTP adecuada. 
# Este archivo es fundamental para el funcionamiento de la lógica de negocio de la aplicación.

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Psicologo, Cita
from .forms import FormularioLogin, PsicologoForm, CitaForm

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Función para dividir el texto en líneas que se ajusten al ancho de la página
def dividir_texto_en_lineas(texto, max_width, font_size, canvas):
    palabras = texto.split(' ')
    lineas = []
    linea_actual = ''
    for palabra in palabras:
        if canvas.stringWidth(linea_actual + ' ' + palabra, "Helvetica", font_size) < max_width:
            linea_actual += ' ' + palabra if linea_actual else palabra
        else:
            lineas.append(linea_actual)
            linea_actual = palabra
    if linea_actual:
        lineas.append(linea_actual)
    return lineas

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Vista para descargar todas las citas en PDF, solo accesible para administradores
@staff_member_required
def descargar_todas_citas_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=todas_citas.pdf'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    margin = 40
    max_width = width - 2 * margin
    y_position = height - margin

    p.setFont("Helvetica", 12)
    p.drawString(margin, y_position, "Todas las Citas de Psicólogos")
    y_position -= 20
    
    citas = Cita.objects.filter(completa=False)

    for cita in citas:
        texto = f"Psicólogo: {cita.psicologo.nombre} - Fecha: {cita.fecha} - Hora: {cita.hora} - Paciente: {cita.paciente} - Contacto: {cita.contacto} - Modalidad: {cita.modalidad}"
        lineas = dividir_texto_en_lineas(texto, max_width, 12, p)
        for linea in lineas:
            if y_position < margin:
                p.showPage()
                y_position = height - margin
                p.setFont("Helvetica", 12)
            p.drawString(margin, y_position, linea)
            y_position -= 15

    p.showPage()
    p.save()
    return response

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Vista para descargar las citas pendientes en PDF, accesible para psicólogos autenticados
@login_required(login_url='vista_login')
def descargar_citas_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=citas_pendientes.pdf'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    margin = 40
    max_width = width - 2 * margin
    y_position = height - margin

    p.setFont("Helvetica", 12)
    p.drawString(margin, y_position, f"Citas Pendientes de {request.user.nombre}")
    y_position -= 20

    # Ajuste aquí para filtrar solo las citas pendientes
    citas = Cita.objects.filter(psicologo=request.user, completa=False)

    for cita in citas:
        texto = f"Fecha: {cita.fecha} - Hora: {cita.hora} - Paciente: {cita.paciente} - Contacto: {cita.contacto} - Modalidad: {cita.modalidad}"
        lineas = dividir_texto_en_lineas(texto, max_width, 12, p)
        for linea in lineas:
            if y_position < margin:
                p.showPage()
                y_position = height - margin
                p.setFont("Helvetica", 12)
            p.drawString(margin, y_position, linea)
            y_position -= 15

    p.showPage()
    p.save()
    return response

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Vista para mostrar la interfaz del psicólogo con sus citas pendientes
@login_required(login_url='vista_login')
def mostrar_interfaz_psicologo(request):
    psicologo = request.user
    citas_pendientes = Cita.objects.filter(psicologo=psicologo, completa=False)
    citas_completadas = Cita.objects.filter(psicologo=psicologo, completa=True)

    if request.method == 'POST':
        enlace_reunion = request.POST.get('enlace_reunion')
        direccion_presencial = request.POST.get('direccion_presencial')
        psicologo.enlace_reunion = enlace_reunion
        psicologo.direccion_presencial = direccion_presencial
        psicologo.save()
        return redirect('interfaz_psicologo')

    return render(request, 'interfaz_psicologo.html', {
        'psicologo': psicologo,
        'citas_pendientes': citas_pendientes,
        'citas_completadas': citas_completadas
    })

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Vista para mostrar el menú principal
def mostrar_menu_principal(request):
    return render(request, 'menu_principal.html')

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Vista para manejar el inicio de sesión de usuarios
def vista_login(request):
    mensaje_error = None
    if request.method == 'POST':
        formulario = FormularioLogin(request.POST)
        if formulario.is_valid():
            correo = formulario.cleaned_data['correo']
            contraseña = formulario.cleaned_data['contraseña']
            usuario = authenticate(request, username=correo, password=contraseña)
            if usuario is not None:
                login(request, usuario)
                if usuario.is_superuser:
                    return redirect('vista_superusuario')
                elif usuario.es_psicologo:
                    return redirect('interfaz_psicologo')
                else:
                    return redirect('interfaz_paciente')
            else:
                mensaje_error = "Correo o contraseña incorrectos."
    else:
        formulario = FormularioLogin()
    return render(request, 'login.html', {'formulario': formulario, 'mensaje_error': mensaje_error})

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Vista para mostrar la interfaz del paciente y asignar citas a psicólogos disponibles
def mostrar_interfaz_paciente(request):
    psicologos = Psicologo.objects.filter(es_psicologo=True)
    mensaje_error = None
    horas_disponibles = []
    fecha_seleccionada = None
    psicologo_seleccionado = None

    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            hora = form.cleaned_data['hora']
            paciente = form.cleaned_data['paciente']
            contacto = request.POST.get('contacto')
            modalidad = request.POST.get('modalidad')
            psicologo_id = request.POST.get('psicologo')

            try:
                psicologo_asignado = Psicologo.objects.get(id=psicologo_id)
            except Psicologo.DoesNotExist:
                messages.error(request, f"El psicólogo seleccionado con ID {psicologo_id} no existe.")
                return render(request, 'interfaz_paciente.html', {
                    'form': form,
                    'psicologos': psicologos,
                    'horas_disponibles': horas_disponibles,
                    'fecha_seleccionada': fecha,
                    'psicologo_seleccionado': psicologo_id
                })

            if not Cita.objects.filter(psicologo=psicologo_asignado, fecha=fecha, hora=hora).exists():
                Cita.objects.create(psicologo=psicologo_asignado, fecha=fecha, hora=hora, paciente=paciente, contacto=contacto, modalidad=modalidad)
                messages.success(request, "Cita agendada con éxito.")
                return redirect('interfaz_paciente')
            else:
                messages.error(request, "El psicólogo seleccionado no está disponible para la fecha y hora seleccionadas.")
        else:
            messages.error(request, "Por favor, corrija los errores en el formulario.")

    else:
        form = CitaForm()

    if request.method == 'GET':
        psicologo_id = request.GET.get('psicologo')
        fecha = request.GET.get('fecha')
        if psicologo_id and fecha:
            horas_disponibles = get_horas_disponibles(psicologo_id, fecha)
            fecha_seleccionada = fecha
            psicologo_seleccionado = psicologo_id
        elif psicologo_id:
            psicologo_seleccionado = psicologo_id

    return render(request, 'interfaz_paciente.html', {
        'form': form,
        'psicologos': psicologos,
        'horas_disponibles': horas_disponibles,
        'fecha_seleccionada': fecha_seleccionada,
        'psicologo_seleccionado': psicologo_seleccionado
    })

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Vista para cerrar la sesión del usuario
def vista_logout(request):
    logout(request)
    return redirect('menu_principal')

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Vista para redirigir a la interfaz del psicólogo si el usuario está autenticado como psicólogo
def soy_psicologo(request):
    if request.user.is_authenticated:
        return redirect('interfaz_psicologo')
    else:
        return redirect('vista_login')

#-----------------------------------------------------------------------------------------------------------------------------------------------

def get_horas_disponibles(psicologo_id, fecha):
    horas_totales = [f"{h:02}:00" for h in range(9, 18)]  # Horas de 9:00 a 17:00
    citas = Cita.objects.filter(psicologo_id=psicologo_id, fecha=fecha).values_list('hora', flat=True)
    horas_ocupadas = [hora.strftime('%H:%M') for hora in citas]
    horas_disponibles = [hora for hora in horas_totales if hora not in horas_ocupadas]
    return horas_disponibles

#-----------------------------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='vista_login')
def marcar_cita_completa(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    cita.completa = True
    cita.save()
    return redirect('interfaz_psicologo')

#-----------------------------------------------------------------------------------------------------------------------------------------------

def consultar_cita(request):
    mensaje_error = None
    citas = []
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        contacto = request.POST.get('contacto')
        citas = Cita.objects.filter(paciente=nombre, contacto=contacto, completa=False)
        if not citas:
            mensaje_error = "No se encontró ninguna cita con los datos proporcionados."
    return render(request, 'consultar_cita.html', {'mensaje_error': mensaje_error, 'citas': citas})

#-----------------------------------------------------------------------------------------------------------------------------------------------

def modificar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    psicologos = Psicologo.objects.filter(es_psicologo=True)
    horas_disponibles = []

    if request.method == 'POST':
        cita.psicologo_id = request.POST.get('psicologo')
        cita.fecha = request.POST.get('fecha')
        cita.hora = request.POST.get('hora')
        cita.modalidad = request.POST.get('modalidad')
        cita.save()
        return redirect('consultar_cita')

    psicologo_id = request.GET.get('psicologo', cita.psicologo_id)
    fecha = request.GET.get('fecha', cita.fecha)
    if psicologo_id and fecha:
        horas_disponibles = get_horas_disponibles(psicologo_id, fecha)

    return render(request, 'modificar_cita.html', {
        'cita': cita,
        'psicologos': psicologos,
        'horas_disponibles': horas_disponibles,
        'fecha_seleccionada': fecha
    })

#-----------------------------------------------------------------------------------------------------------------------------------------------

def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    if request.method == 'POST':
        cita.delete()
        return redirect('consultar_cita')
    return redirect('modificar_cita', cita_id=cita_id)

#-----------------------------------------------------------------------------------------------------------------------------------------------

@login_required
def editar_perfil_psicologo(request):
    if request.method == 'POST':
        form = PsicologoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('interfaz_psicologo')
    else:
        form = PsicologoForm(instance=request.user)
    return render(request, 'editar_perfil_psicologo.html', {'form': form})

#-----------------------------------------------------------------------------------------------------------------------------------------------