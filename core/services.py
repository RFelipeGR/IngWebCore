from reservas.models import Reserva
from administracion.models import Horario

from reservas.models import Reserva
from administracion.models import Horario

from decimal import Decimal


# ----------------------------------------
# 1) Cálculo de ocupación
# ----------------------------------------

def calcular_ocupacion(horario):
    capacidad = horario.bus.capacidad
    usados = Reserva.objects.filter(horario=horario).count()

    if capacidad == 0:
        return 0, usados, capacidad

    ocupacion = (usados / capacidad) * 100
    return ocupacion, usados, capacidad

# ----------------------------------------
# 2) Regla de negocio: umbral mínimo
#    Devuelve True si YA CUMPLE el mínimo.
# ----------------------------------------

def cumple_umbral(horario, umbral=30):
    """
    Devuelve True si la ocupación cumple el mínimo (>= umbral),
    False si está por debajo (CRÍTICO).
    """
    ocupacion, usados, capacidad = calcular_ocupacion(horario)

    if capacidad == 0:
        return False

    # 👉 OK cuando está en o por encima del umbral
    return ocupacion >= umbral



# ---------------------------------------------------
# 3) Buscar rutas alternativas (transferencias)
# ---------------------------------------------------

def buscar_opciones_transferencia(horario_actual):
    """
    Busca otros horarios del MISMO día y MISMA ruta,
    pero en diferente hora.
    """
    return Horario.objects.filter(
        ruta=horario_actual.ruta
    ).exclude(id=horario_actual.id).order_by("hora_salida")


# ---------------------------------------------------
# 4) Ejecutar transferencia de reservas
# ---------------------------------------------------

def ejecutar_transferencia(reservas, horario_destino):
    """
    Mueve reservas seleccionadas a otro horario.
    """
    for r in reservas:
        r.horario = horario_destino
        r.save()

    return True





# core/services.py

# ----------------------------------------
# TARIFAS APROXIMADAS POR RUTA
# (simulación para el CORE de negocio)
# ----------------------------------------
TARIFAS_POR_RUTA = {
    ("Quito", "Guayaquil"): Decimal("18.00"),
    ("Quito", "Cuenca"): Decimal("16.00"),
    ("Quito", "Esmeraldas"): Decimal("14.00"),
    ("Quito", "Machala"): Decimal("17.00"),
    ("Guayaquil", "Quito"): Decimal("18.00"),
    ("Cuenca", "Quito"): Decimal("16.00"),
    # puedes agregar más rutas si quieres
}


def obtener_tarifa_ruta(ruta):
    """
    Devuelve una tarifa aproximada en dólares
    según la ruta origen-destino.
    Si no está en el mapa, usa un valor por defecto.
    """
    clave = (ruta.origen, ruta.destino)
    return TARIFAS_POR_RUTA.get(clave, Decimal("15.00"))


def calcular_ocupacion(horario):
    """
    Devuelve (ocupación_en_porcentaje, usados, capacidad_total)
    """
    capacidad = horario.bus.capacidad
    usados = Reserva.objects.filter(horario=horario).count()

    if capacidad == 0:
        return 0, 0, 0

    ocupacion = (usados / capacidad) * 100
    return ocupacion, usados, capacidad


def factor_urgencia(ocupacion):
    """
    Entre más ocupación tenga el bus que transfiere,
    más urgente es la situación, mayor el factor.
    """
    if ocupacion < 30:
        return Decimal("1.0")
    elif ocupacion < 80:
        return Decimal("1.2")
    else:
        return Decimal("1.5")


def calcular_costos_negociacion(horario_origen, horario_destino, cantidad_pasajeros):
    """
    Calcula todos los valores de la negociación entre cooperativas.
    Devuelve un diccionario listo para usar en la plantilla.
    """
    tarifa_origen = obtener_tarifa_ruta(horario_origen.ruta)
    tarifa_destino = obtener_tarifa_ruta(horario_destino.ruta)

    # Diferencia de tarifas (lo que "pierde" o "gana" la otra empresa)
    diferencia = tarifa_destino - tarifa_origen

    # Costos operativos estimados (simples, solo para demo de CORE)
    costos_operativos = Decimal("4.80")

    ocupacion, usados, capacidad = calcular_ocupacion(horario_origen)
    f_urgencia = factor_urgencia(ocupacion)

    # Compensación sugerida por pasajero
    # (tarifa destino + costos + max(0, diferencia)) * factor
    base = tarifa_destino + costos_operativos + max(Decimal("0.00"), diferencia)
    compensacion_por_pasajero = base * f_urgencia

    total_sugerido = compensacion_por_pasajero * Decimal(cantidad_pasajeros)

    return {
        "tarifa_origen": tarifa_origen,
        "tarifa_destino": tarifa_destino,
        "diferencia": diferencia,
        "costos_operativos": costos_operativos,
        "ocupacion": ocupacion,
        "usados": usados,
        "capacidad": capacidad,
        "factor_urgencia": f_urgencia,
        "compensacion_por_pasajero": compensacion_por_pasajero,
        "total_sugerido": total_sugerido,
    }
