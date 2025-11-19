import random
from administracion.models import Horario
from reservas.models import Reserva


def generar_reservas_dummy():
    """
    Genera 20 reservas automáticas por cada horario.
    Solo si ese horario no tiene reservas aún.
    """
    horarios = Horario.objects.all()

    for h in horarios:

        # Evitar duplicados
        if Reserva.objects.filter(horario=h).exists():
            continue

        capacidad = h.bus.capacidad  # ← AHORA VIENE DEL BUS

        # Generar 20 reservas dummy o tantas como permita la capacidad
        num_reservas = min(20, capacidad)

        for i in range(num_reservas):
            nombre = f"Pasajero {i+1}"
            cedula = f"{random.randint(1000000000, 9999999999)}"
            asiento = i + 1  # así evitamos duplicados

            Reserva.objects.create(
                horario=h,
                nombre_pasajero=nombre,
                cedula=cedula,
                asiento=asiento
            )






def generar_reservas_para_un_horario(horario_id, cantidad):
    """
    Genera 'cantidad' de reservas para un horario específico.
    No borra reservas existentes; solo agrega nuevas.
    """


    try:
        horario = Horario.objects.get(id=horario_id)
    except Horario.DoesNotExist:
        return f"❌ El horario con ID {horario_id} no existe."

    capacidad = horario.bus.capacidad
    reservas_existentes = Reserva.objects.filter(horario=horario).count()

    disponibles = capacidad - reservas_existentes
    if disponibles <= 0:
        return "⚠ No hay asientos disponibles."

    cantidad_real = min(cantidad, disponibles)

    inicio_asiento = reservas_existentes + 1

    for i in range(cantidad_real):
        nombre = f"Pasajero Extra {i+1}"
        cedula = f"{random.randint(1000000000, 9999999999)}"
        asiento = inicio_asiento + i

        Reserva.objects.create(
            horario=horario,
            nombre_pasajero=nombre,
            cedula=cedula,
            asiento=asiento
        )

    return f"✔ Se agregaron {cantidad_real} reservas al horario {horario_id}."
