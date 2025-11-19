from reservas.models import Reserva
from administracion.models import Horario

from reservas.models import Reserva
from administracion.models import Horario

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

def cumple_umbral(horario, umbral=40):
    """
    True  -> el bus YA cumple el mínimo de ocupación (OK)
    False -> el bus NO llega al mínimo (CRÍTICO / requiere negociación)
    """
    ocupacion, usados, capacidad = calcular_ocupacion(horario)
    return ocupacion >= umbral



# ---------------------------------------------------
# 2) Buscar rutas alternativas (transferencias)
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
# 3) Ejecutar transferencia de reservas
# ---------------------------------------------------

def ejecutar_transferencia(reservas, horario_destino):
    """
    Mueve reservas seleccionadas a otro horario.
    """
    for r in reservas:
        r.horario = horario_destino
        r.save()

    return True
