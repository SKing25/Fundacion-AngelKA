# Este archivo se utiliza para definir los modelos que representan las estructuras de datos de tu aplicación.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.conf import settings

# Definir un manager para el modelo personalizado de psicólogo
# models.py
# models.py


class PsicologoManager(BaseUserManager):
    def create_user(self, correo, nombre, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico es obligatorio')
        correo = self.normalize_email(correo)
        extra_fields.setdefault('es_psicologo', True)  # Establecer es_psicologo como True por defecto
        user = self.model(correo=correo, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('es_psicologo', False)  # Superusuarios no son psicólogos

        return self.create_user(correo, nombre, password, **extra_fields)

class Psicologo(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    es_psicologo = models.BooleanField(default=True)  # Añadir campo es_psicologo

    objects = PsicologoManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.nombre

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password


# Modelo que representa una Cita
# models.py

# models.py

# models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Cita(models.Model):
    psicologo = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    paciente = models.CharField(max_length=255)
    completa = models.BooleanField(default=False)  # Nuevo campo

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.paciente} (Completa: {self.completa})"



    class Meta:
        unique_together = ('psicologo', 'fecha', 'hora')