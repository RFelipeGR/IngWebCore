from django.db import models

# Create your models here.
# buses/models.py
class Bus(models.Model):
    cooperativa = models.ForeignKey(Cooperativa, on_delete=models.CASCADE)
    placa = models.CharField(max_length=10)
    capacidad = models.PositiveIntegerField()
    # ...

# rutas/models.py
class Ruta(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    # ...

# horarios/models.py
class Horario(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    hora_salida = models.DateTimeField()
    capacidad_total = models.PositiveIntegerField()
    pasajeros_actuales = models.PositiveIntegerField(default=0)
    # ...
