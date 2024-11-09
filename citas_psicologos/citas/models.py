# El archivo models.py en una aplicación de Django se utiliza para definir los modelos de datos que representan las estructuras de las tablas 
# en la base de datos. Estos modelos son clases de Python que Django convierte en tablas de la base de datos. Cada modelo puede contener campos, 
# métodos y propiedades que definen el comportamiento y las relaciones entre los datos.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password

#-----------------------------------------------------------------------------------------------------------------------------------------------

class PsicologoManager(BaseUserManager):
    def create_user(self, correo, nombre, password=None, **extra_fields):
        if not correo:
            raise ValueError('El usuario debe tener un correo electrónico')
        correo = self.normalize_email(correo)
        usuario = self.model(correo=correo, nombre=nombre, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        
        return self.create_user(correo, nombre, password, **extra_fields)

#-----------------------------------------------------------------------------------------------------------------------------------------------

class Psicologo(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    es_psicologo = models.BooleanField(default=True)
    enlace_reunion = models.URLField(max_length=200, blank=True, null=True) 
    direccion_presencial = models.CharField(max_length=255, blank=True, null=True)

    objects = PsicologoManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.nombre

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def get_by_natural_key(self, correo):
        return self.get(correo=correo)

#-----------------------------------------------------------------------------------------------------------------------------------------------

class Cita(models.Model):
    psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE)
    paciente = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    modalidad = models.CharField(max_length=10, choices=[('Presencial', 'Presencial'), ('Virtual', 'Virtual')])
    completa = models.BooleanField(default=False)
    enlace_reunion = models.URLField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('psicologo', 'fecha', 'hora')

#-----------------------------------------------------------------------------------------------------------------------------------------------
