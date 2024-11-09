# El archivo forms.py en una aplicación de Django se utiliza para definir formularios que se basan en modelos de la aplicación 
# o que son independientes de los modelos. Estos formularios se utilizan para gestionar 
# la entrada de datos del usuario de manera estructurada y segura.

from django import forms
from .models import Psicologo, Cita

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Definir un formulario de inicio de sesión
class FormularioLogin(forms.Form):
    correo = forms.EmailField()
    contraseña = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['correo', 'contraseña']

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Definir un formulario de registro basado en el modelo Psicologo
class FormularioRegistro(forms.ModelForm):
    # Meta clase para especificar el modelo y los campos incluidos en el formulario
    class Meta:
        model = Psicologo
        fields = ['nombre', 'correo', 'contraseña']

    # Campo de contraseña renderizado como campo de entrada de tipo contraseña
    contraseña = forms.CharField(widget=forms.PasswordInput)
    # Campo adicional para confirmar la contraseña
    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    # Método para validar que ambas contraseñas coinciden
    def clean_confirmar_contraseña(self):
        cd = self.cleaned_data
        if cd['contraseña'] != cd['confirmar_contraseña']:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cd['confirmar_contraseña']

    # Método para guardar el usuario con la contraseña encriptada
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["contraseña"])
        if commit:
            user.save()
        return user

#-----------------------------------------------------------------------------------------------------------------------------------------------

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha', 'hora', 'paciente']

    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    HORA_CHOICES = [(f"{h:02}:00", f"{h:02}:00") for h in range(0, 24)]
    hora = forms.ChoiceField(choices=HORA_CHOICES)

#-----------------------------------------------------------------------------------------------------------------------------------------------

class PsicologoForm(forms.ModelForm):
    class Meta:
        model = Psicologo
        fields = ['nombre', 'correo', 'enlace_reunion', 'direccion_presencial']

#-----------------------------------------------------------------------------------------------------------------------------------------------