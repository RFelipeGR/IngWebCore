import random
from django.utils import timezone
from reservas.models import Reserva
from administracion.models import Bus, Horario


NOMBRES = [
    "Juan", "María", "Pedro", "Ana", "Luis",
    "Carla", "David", "Lucía", "Fernando", "Sofía",
    "Andrés", "Valeria", "Pablo", "Gabriela", "Mateo",
]

APELLIDOS = [
    "García", "Pérez", "Lopez", "Sánchez", "Torres",
    "Rivera", "Romero", "Ortiz", "Cedeño", "Castro"
]


def crear_reservas_para_horario(horario, cantidad=20):
    """
    Crea exactamente 'cantidad' reservas dummy en el horario dado.
    Respeta la capacidad del bus y genera asientos únicos.
    """

    print(f" → Creando {cantidad} reservas para horario #{horario.id} - Bus {horario.bus.placa}")

    capacidad = horario.bus.capacidad

    # Ajusta el número si el bus tiene menos capacidad
    cantidad = min(cantidad, capacidad)

    # Limpia reservas anteriores
    Reserva.objects.filter(horario=horario).delete()

    # Generar lista de asientos disponibles
    asientos = list(range(1, capacidad + 1))
    random.shuffle(asientos)

    for i in range(cantidad):
        nombre = random.choice(NOMBRES)
        apellido = random.choice(APELLIDOS)
        nombre_completo = f"{nombre} {apellido}"

        cedula = f"{random.randint(1000000000, 9999999999)}"

        Reserva.objects.create(
            horario=horario,
            asiento=asientos[i],
            nombre_pasajero=nombre_completo,
            cedula=cedula,
        )

    print(f" ✔ {cantidad} reservas creadas correctamente.")


def cargar_datos_reales():
    """
    Llena TODOS los horarios reales con 20 reservas.
    """

    print("\n==============================")
    print("  CARGANDO 20 RESERVAS POR HORARIO...")
    print("==============================\n")

    # 1. Borrar todas las reservas previas
    Reserva.objects.all().delete()
    print("✔ Reservas anteriores eliminadas.\n")

    # 2. Obtener todos los horarios
    horarios = Horario.objects.all()

    if not horarios.exists():
        print("⚠ No hay horarios en la base de datos.")
        return False

    print(f"Se encontraron {horarios.count()} horarios.\n")

    # 3. Crear 20 reservas por cada horario
    for h in horarios:
        crear_reservas_para_horario(h, cantidad=20)

    print("\n==============================")
    print("✔ TODOS LOS HORARIOS TIENEN 20 PASAJEROS")
    print("==============================\n")
    return True
