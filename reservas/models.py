from django.db import models
from administracion.models import Horario

class Reserva(models.Model):
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    nombre_pasajero = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10)
    asiento = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre_pasajero} - Asiento {self.asiento}"
