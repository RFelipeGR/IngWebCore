from django.db import models
from django.conf import settings
from administracion.models import Horario
from django.db import models
from administracion.models import Cooperativa, Bus, Ruta



class TransferLog(models.Model):
    ESTADOS = (
        ("OK", "Transferencia exitosa"),
        ("ERROR", "Transferencia fallida"),
    )

    fecha = models.DateTimeField(auto_now_add=True)

    # Quién hizo la operación (opcional)
    operador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    origen = models.ForeignKey(
        Horario,
        related_name="logs_origen",
        on_delete=models.SET_NULL,
        null=True
    )
    destino = models.ForeignKey(
        Horario,
        related_name="logs_destino",
        on_delete=models.SET_NULL,
        null=True
    )

    # IDs de reservas involucradas en la transferencia (lista)
    reservas = models.JSONField()

    cantidad_pasajeros = models.PositiveIntegerField()

    # Capacidad libre antes/después
    capacidad_origen_antes = models.IntegerField(null=True, blank=True)
    capacidad_origen_despues = models.IntegerField(null=True, blank=True)
    capacidad_destino_antes = models.IntegerField(null=True, blank=True)
    capacidad_destino_despues = models.IntegerField(null=True, blank=True)

    estado = models.CharField(max_length=10, choices=ESTADOS)
    mensaje = models.TextField(blank=True)

    def __str__(self):
        return f"Log transferencia {self.id} - {self.estado}"




class IncidenteCooperativa(models.Model):
    cooperativa = models.ForeignKey(Cooperativa, on_delete=models.CASCADE, null=True, blank=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True, blank=True)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, null=True, blank=True)

    descripcion = models.TextField()
    activo = models.BooleanField(default=True)

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Incidente {self.cooperativa} - {self.fecha:%Y-%m-%d}"
