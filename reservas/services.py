import random
from administracion.models import Horario
from reservas.models import Reserva


def generar_reservas_dummy():
    """
    Genera reservas dummy SIN duplicar asientos ni pasajeros.
    Solo crea reservas donde faltan.
    """
    horarios = Horario.objects.all()

    for h in horarios:

        capacidad = h.bus.capacidad

        # Asientos ya ocupados (evita duplicados)
        asientos_ocupados = set(
            Reserva.objects.filter(horario=h)
            .values_list("asiento", flat=True)
        )

        # Crear máximo 20 o lo que falte
        faltantes = capacidad - len(asientos_ocupados)
        crear = min(20, faltantes)

        # Si ya no hay espacio, saltar
        if crear <= 0:
            continue

        # Generar nuevos pasajeros en los asientos disponibles
        siguiente_asiento = 1

        for _ in range(crear):

            # Buscar siguiente asiento libre
            while siguiente_asiento in asientos_ocupados:
                siguiente_asiento += 1

            # Generar pasajero único
            nombre = f"Pasajero {random.randint(1000, 9999)}"
            cedula = f"{random.randint(1000000000, 9999999999)}"

            Reserva.objects.create(
                horario=h,
                nombre_pasajero=nombre,
                cedula=cedula,
                asiento=siguiente_asiento
            )

            # Marcar asiento como ocupado
            asientos_ocupados.add(siguiente_asiento)


def generar_reservas_para_un_horario(horario_id, cantidad):
    """
    Genera reservas adicionales sin duplicar asientos ni sobrescribir datos.
    """

    try:
        horario = Horario.objects.get(id=horario_id)
    except Horario.DoesNotExist:
        return f"❌ El horario con ID {horario_id} no existe."

    capacidad = horario.bus.capacidad

    asientos_ocupados = set(
        Reserva.objects.filter(horario=horario)
        .values_list("asiento", flat=True)
    )

    disponibles = capacidad - len(asientos_ocupados)
    crear = min(cantidad, disponibles)

    if crear <= 0:
        return "⚠ No hay asientos disponibles."

    siguiente_asiento = 1

    for _ in range(crear):

        while siguiente_asiento in asientos_ocupados:
            siguiente_asiento += 1

        nombre = f"Pasajero Extra {random.randint(1000, 9999)}"
        cedula = f"{random.randint(1000000000, 9999999999)}"

        Reserva.objects.create(
            horario=horario,
            nombre_pasajero=nombre,
            cedula=cedula,
            asiento=siguiente_asiento
        )

        asientos_ocupados.add(siguiente_asiento)

    return f"✔ Se agregaron {crear} reservas al horario {horario_id}."




def asignar_asiento_libre(horario):
    """
    Retorna el primer asiento libre en un horario.
    Si no hay asientos disponibles → retorna None.
    """

    capacidad = horario.bus.capacidad

    # Asientos ocupados
    ocupados = set(
        Reserva.objects.filter(horario=horario)
        .values_list("asiento", flat=True)
    )

    # Buscar el primer asiento libre
    for num in range(1, capacidad + 1):
        if num not in ocupados:
            return num

    return None  # Bus lleno
