# El archivo models.py en una aplicación de Django se utiliza para definir los modelos de datos que representan las estructuras de las tablas 
# en la base de datos. Estos modelos son clases de Python que Django convierte en tablas de la base de datos. Cada modelo puede contener campos, 
# métodos y propiedades que definen el comportamiento y las relaciones entre los datos.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Definir un manager personalizado para el modelo Psicologo
class PsicologoManager(BaseUserManager):
    # Método para crear un usuario estándar
    def create_user(self, correo, nombre, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico es obligatorio')
        correo = self.normalize_email(correo)
        extra_fields.setdefault('es_psicologo', True)
        user = self.model(correo=correo, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Método para crear un superusuario
    def create_superuser(self, correo, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('es_psicologo', False)
        return self.create_user(correo, nombre, password, **extra_fields)

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Definir el modelo Psicologo que hereda de AbstractBaseUser y PermissionsMixin para personalizar la autenticación
class Psicologo(AbstractBaseUser, PermissionsMixin):
    # Definición de los campos del modelo
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    es_psicologo = models.BooleanField(default=True)

    # Usar el manager personalizado para este modelo
    objects = PsicologoManager()

    # Definir el campo de nombre de usuario para autenticación
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    # Método para representar el objeto como cadena
    def __str__(self):
        return self.nombre

    # Método para establecer la contraseña del usuario
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Obtener el modelo de usuario actual de Django
User = get_user_model()

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Definir el modelo Cita para gestionar las citas
class Cita(models.Model):
    psicologo = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    paciente = models.CharField(max_length=255)
    completa = models.BooleanField(default=False)  # Nuevo campo para marcar la cita como completa

    # Método para representar el objeto como cadena
    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.paciente} (Completa: {self.completa})"

#-----------------------------------------------------------------------------------------------------------------------------------------------

# Definir la clase Meta para el modelo Cita
class Meta:
    unique_together = ('psicologo', 'fecha', 'hora')  # Asegurar que cada cita es única por psicólogo, fecha y hora

#-----------------------------------------------------------------------------------------------------------------------------------------------
