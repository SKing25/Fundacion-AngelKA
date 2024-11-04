from django import forms
from .models import Psicologo, Cita

class FormularioLogin(forms.Form):
    correo = forms.EmailField(label='Correo Electrónico', max_length=100)
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class FormularioRegistro(forms.ModelForm):
    class Meta:
        model = Psicologo
        fields = ['nombre', 'correo', 'contraseña']

    contraseña = forms.CharField(widget=forms.PasswordInput)
    confirmar_contraseña = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    def clean_confirmar_contraseña(self):
        cd = self.cleaned_data
        if cd['contraseña'] != cd['confirmar_contraseña']:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cd['confirmar_contraseña']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["contraseña"])
        if commit:
            user.save()
        return user

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha', 'hora', 'paciente']

    HORA_CHOICES = [(f"{h:02}:00", f"{h:02}:00") for h in range(0, 24)]
    hora = forms.ChoiceField(choices=HORA_CHOICES)
