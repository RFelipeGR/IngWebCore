from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from administracion.models import Operador, Horario
from reservas.models import Reserva
from core.services import cumple_umbral, buscar_opciones_transferencia, ejecutar_transferencia
from core.services import cumple_umbral, buscar_opciones_transferencia
from reservas.services import generar_reservas_dummy

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from administracion.models import Horario
from reservas.models import Reserva
from core.services import cumple_umbral, buscar_opciones_transferencia, ejecutar_transferencia

from core.services import calcular_ocupacion, cumple_umbral
from django.contrib.auth import logout
from django.shortcuts import redirect






@login_required
def panel_operador(request):
    operador = Operador.objects.get(user=request.user)
    cooperativa = operador.cooperativa

    horarios = Horario.objects.filter(bus__cooperativa=cooperativa)

    data = []
    for h in horarios:
        ocupacion, usados, total = calcular_ocupacion(h)
        cumple = cumple_umbral(h)   # ← ahora True = OK

        estado = "OK" if cumple else "CRÍTICO"

        data.append({
            "horario": h,
            "ocupacion": round(ocupacion, 2),
            "usados": usados,
            "total": total,
            "estado": estado,
        })

    return render(request, "reservas/panel_operador.html", {
        "cooperativa": cooperativa,
        "data": data,
    })



@login_required
def iniciar_negociacion(request, reserva_id):
    operador = Operador.objects.get(user=request.user)

    reserva = get_object_or_404(
        Reserva,
        id=reserva_id,
        horario__bus__cooperativa=operador.cooperativa
    )

    opciones = buscar_opciones_transferencia(reserva)

    return render(request, "reservas/negociacion.html", {
        "reserva": reserva,
        "opciones": opciones
    })


@login_required
def transferir_pasajeros(request, reserva_id, horario_id):
    operador = Operador.objects.get(user=request.user)

    reserva = get_object_or_404(
        Reserva,
        id=reserva_id,
        horario__bus__cooperativa=operador.cooperativa
    )

    horario_destino = get_object_or_404(Horario, id=horario_id)

    if request.method == "POST":
        cantidad = int(request.POST.get("cantidad"))
        ejecutar_transferencia(reserva, horario_destino, cantidad)
        return render(request, "reservas/transferencia_exitosa.html")

    # Acceso sin POST → volver al panel
    return redirect('panel_operador')


@login_required
def detalle_reserva(request, id):
    horario = get_object_or_404(Horario, id=id)
    reservas = Reserva.objects.filter(horario=horario).order_by("asiento")

    contexto = {
        "horario": horario,
        "reservas": reservas,
    }
    return render(request, "reservas/detalle_reserva.html", contexto)


@login_required
def transferencias(request, id):
    horario_actual = get_object_or_404(Horario, id=id)

    opciones = buscar_opciones_transferencia(horario_actual)
    reservas = Reserva.objects.filter(horario=horario_actual).order_by("asiento")

    if request.method == "POST":
        destino_id = request.POST.get("destino")
        seleccionados = request.POST.getlist("reservas")

        horario_destino = get_object_or_404(Horario, id=destino_id)
        reservas_obj = Reserva.objects.filter(id__in=seleccionados)

        ejecutar_transferencia(reservas_obj, horario_destino)

        return render(request, "reservas/transferencia_exitosa.html", {
            "destino": horario_destino
        })

    return render(request, "reservas/transferencias.html", {
        "horario": horario_actual,
        "opciones": opciones,
        "reservas": reservas
    })



@login_required
def estadisticas_reserva(request, id):
    horario = get_object_or_404(Horario, id=id)

    # Cálculo con la lógica del core
    ocupacion, usados, total = calcular_ocupacion(horario)
    cumple = cumple_umbral(horario)  # True = OK, False = CRÍTICO

    estado = "OK" if cumple else "CRÍTICO"

    return render(request, "reservas/estadisticas_reserva.html", {
        "horario": horario,
        "ocupacion": round(ocupacion, 2),
        "usados": usados,
        "total": total,
        "estado": estado,
    })



def operador_logout(request):
    logout(request)
    return redirect('login')   # Ajusta si tu login tiene otro nombre