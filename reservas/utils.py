import random
from administracion.models import Horario
from reservas.models import Reserva

def resetear_reservas():
    # Limpiar todas las reservas
    Reserva.objects.all().delete()

    horarios = Horario.objects.all()

    for h in horarios:
        capacidad = h.bus.capacidad
        cantidad = min(20, capacidad)

        for i in range(1, cantidad + 1):
            Reserva.objects.create(
                horario=h,
                nombre_pasajero=f"Pasajero {i}",
                cedula=str(random.randint(1000000000, 9999999999)),
                asiento=i
            )
