from django.db import models

class Psicologo(models.Model):
    nombre = models.CharField(max_length=100)

class Cita(models.Model):
    psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    paciente = models.CharField(max_length=100)

    class Meta:
        unique_together = ('psicologo', 'fecha', 'hora')
