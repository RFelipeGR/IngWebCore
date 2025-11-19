from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.generic import ListView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Count
from .forms import OperadorEditForm
from django.shortcuts import get_object_or_404

from .forms import (
    LoginForm,
    CooperativaForm,
    BusForm,
    RutaForm,
    HorarioForm,
    OperadorCreateForm,
)
from .models import Cooperativa, Bus, Ruta, Horario, Operador
from reservas.models import Reserva


# =======================
# LOGIN / LOGOUT
# =======================

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # SUPERADMIN (is_staff === True)
                if user.is_staff:
                    return redirect('panel_admin')  # → /panel/

                # OPERADOR (is_staff == False BUT exists in Operador)
                try:
                    Operador.objects.get(user=user)
                    return redirect('panel_operador')  # → /panel/operador/panel/
                except Operador.DoesNotExist:
                    # Usuario válido pero NO es staff ni operador
                    messages.error(request, "Tu cuenta no tiene un rol asignado.")
                    return redirect('login')

            else:
                form.add_error(None, "Credenciales incorrectas")
    else:
        form = LoginForm()

    return render(request, 'administracion/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# =======================
# HELPERS
# =======================

def _solo_staff(request):
    """Verifica que el usuario sea staff (superadmin)."""
    if not request.user.is_staff:
        return False
    return True


# =======================
# PANELES HOME
# =======================

@login_required
def panel_home(request):
    """
    Punto de entrada general:
    - Si es superadmin → panel_admin
    - Si es operador → panel_operador
    - Si no tiene rol → login con mensaje
    """
    if request.user.is_staff:
        return redirect('panel_admin')

    try:
        Operador.objects.get(user=request.user)
        return redirect('panel_operador')
    except Operador.DoesNotExist:
        messages.error(request, "Tu cuenta no tiene un rol válido.")
        return redirect('login')


@login_required
def usuario_home(request):
    """
    Compatibilidad con la antigua ruta de 'usuario'.
    Ahora simplemente redirige al panel del operador.
    """
    try:
        Operador.objects.get(user=request.user)
        return redirect('panel_operador')
    except Operador.DoesNotExist:
        return redirect('login')


# =======================
# PANEL SUPERADMIN (DASHBOARD)
# =======================

@login_required
def panel_admin(request):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso para ver este panel.")

    total_cooperativas = Cooperativa.objects.count()
    total_buses = Bus.objects.count()
    total_rutas = Ruta.objects.count()
    total_horarios = Horario.objects.count()
    total_reservas = Reserva.objects.count()

    reservas_por_cooperativa = (
        Reserva.objects
        .values('horario__bus__cooperativa__nombre')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    return render(request, 'administracion/panel_admin.html', {
        'total_cooperativas': total_cooperativas,
        'total_buses': total_buses,
        'total_rutas': total_rutas,
        'total_horarios': total_horarios,
        'total_reservas': total_reservas,
        'reservas_por_cooperativa': reservas_por_cooperativa,
    })


# =======================
# VISTAS "ANTIGUAS" TIPO MVC (CLASES)
# =======================

class CooperativaListView(ListView):
    model = Cooperativa
    template_name = 'administracion/cooperativa_list.html'
    context_object_name = 'cooperativas'


class CooperativaCreateView(CreateView):
    model = Cooperativa
    form_class = CooperativaForm
    template_name = 'administracion/cooperativa_form.html'
    success_url = reverse_lazy('cooperativa_list')


class BusListView(ListView):
    model = Bus
    template_name = 'administracion/bus_list.html'
    context_object_name = 'buses'


class BusCreateView(CreateView):
    model = Bus
    form_class = BusForm
    template_name = 'administracion/bus_form.html'
    success_url = reverse_lazy('bus_list')


class ReservaListView(ListView):
    model = Reserva
    template_name = 'administracion/reserva_list.html'
    context_object_name = 'reservas'


class ReservaCreateView(CreateView):
    model = Reserva
    fields = ['horario', 'pasajeros']
    template_name = 'administracion/reserva_form.html'
    success_url = reverse_lazy('reserva_list')


class MonitoreoView(TemplateView):
    template_name = 'administracion/monitoreo.html'


# API auxiliar para obtener buses por cooperativa (antiguo)
@login_required
def buses_por_cooperativa(request):
    cooperativa_id = request.GET.get('cooperativa_id')
    buses = Bus.objects.filter(cooperativa_id=cooperativa_id).values('id', 'placa')
    return JsonResponse(list(buses), safe=False)


# =======================
# CRUD SUPERADMIN (FUNCIONES EN /panel/...)
# =======================

# --- COOPERATIVAS (Panel) ---

@login_required
def cooperativa_list(request):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    cooperativas = Cooperativa.objects.all()
    return render(request, 'administracion/cooperativa_list.html', {
        'cooperativas': cooperativas
    })


@login_required
def cooperativa_create(request):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    if request.method == 'POST':
        form = CooperativaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('super_cooperativa_list')
    else:
        form = CooperativaForm()
    return render(request, 'administracion/cooperativa_form.html', {'form': form})


@login_required
def cooperativa_edit(request, pk):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    cooperativa = get_object_or_404(Cooperativa, pk=pk)
    if request.method == 'POST':
        form = CooperativaForm(request.POST, instance=cooperativa)
        if form.is_valid():
            form.save()
            return redirect('super_cooperativa_list')
    else:
        form = CooperativaForm(instance=cooperativa)
    return render(request, 'administracion/cooperativa_form.html', {'form': form})


@login_required
def cooperativa_delete(request, pk):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    cooperativa = get_object_or_404(Cooperativa, pk=pk)
    if request.method == 'POST':
        cooperativa.delete()
        return redirect('super_cooperativa_list')
    return render(request, 'administracion/cooperativa_confirm_delete.html', {
        'cooperativa': cooperativa
    })


# --- BUSES (Panel) ---

@login_required
def bus_list(request):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    buses = Bus.objects.select_related('cooperativa')
    return render(request, 'administracion/bus_list.html', {'buses': buses})


@login_required
def bus_create(request):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('super_bus_list')
    else:
        form = BusForm()
    return render(request, 'administracion/bus_form.html', {'form': form})


@login_required
def bus_edit(request, pk):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    bus = get_object_or_404(Bus, pk=pk)
    if request.method == 'POST':
        form = BusForm(request.POST, instance=bus)
        if form.is_valid():
            form.save()
            return redirect('super_bus_list')
    else:
        form = BusForm(instance=bus)
    return render(request, 'administracion/bus_form.html', {'form': form})


@login_required
def bus_delete(request, pk):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    bus = get_object_or_404(Bus, pk=pk)
    if request.method == 'POST':
        bus.delete()
        return redirect('super_bus_list')
    return render(request, 'administracion/bus_confirm_delete.html', {'bus': bus})


# --- RUTAS (Panel) ---

@login_required
def ruta_list(request):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    rutas = Ruta.objects.all()
    return render(request, 'administracion/ruta_list.html', {'rutas': rutas})


@login_required
def ruta_create(request):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    if request.method == 'POST':
        form = RutaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('super_ruta_list')
    else:
        form = RutaForm()
    return render(request, 'administracion/ruta_form.html', {'form': form})


@login_required
def ruta_edit(request, pk):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    ruta = get_object_or_404(Ruta, pk=pk)
    if request.method == 'POST':
        form = RutaForm(request.POST, instance=ruta)
        if form.is_valid():
            form.save()
            return redirect('super_ruta_list')
    else:
        form = RutaForm(instance=ruta)
    return render(request, 'administracion/ruta_form.html', {'form': form})


@login_required
def ruta_delete(request, pk):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    ruta = get_object_or_404(Ruta, pk=pk)
    if request.method == 'POST':
        ruta.delete()
        return redirect('super_ruta_list')
    return render(request, 'administracion/ruta_confirm_delete.html', {'ruta': ruta})


# --- HORARIOS (Panel) ---

@login_required
def horario_list(request):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    horarios = Horario.objects.select_related('bus', 'ruta')
    return render(request, 'administracion/horario_list.html', {
        'horarios': horarios
    })


@login_required
def horario_create(request):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('super_horario_list')
    else:
        form = HorarioForm()
    return render(request, 'administracion/horario_form.html', {'form': form})


@login_required
def horario_edit(request, pk):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    horario = get_object_or_404(Horario, pk=pk)
    if request.method == 'POST':
        form = HorarioForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            return redirect('super_horario_list')
    else:
        form = HorarioForm(instance=horario)
    return render(request, 'administracion/horario_form.html', {'form': form})


@login_required
def horario_delete(request, pk):
    if not _solo_staff(request):
        return HttpResponseForbidden("No tienes permiso.")
    horario = get_object_or_404(Horario, pk=pk)
    if request.method == 'POST':
        horario.delete()
        return redirect('super_horario_list')
    return render(request, 'administracion/horario_confirm_delete.html', {'horario': horario})


# --- OPERADORES (Panel) ---

@login_required
def operador_list(request):
    operadores = Operador.objects.select_related("user", "cooperativa")
    return render(request, "administracion/operadores_list.html", {
        "operadores": operadores
    })




@login_required
def operador_create(request):
    if request.method == "POST":
        form = OperadorCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("operador_list")
    else:
        form = OperadorCreateForm()

    return render(request, "administracion/operador_form.html", {"form": form})


@login_required
def operador_edit(request, pk):
    operador = get_object_or_404(Operador, pk=pk)
    user = operador.user

    if request.method == "POST":
        form = OperadorEditForm(request.POST, instance=user)
        nueva_coop = request.POST.get("cooperativa")

        if form.is_valid():
            form.save()

            if nueva_coop:
                operador.cooperativa_id = nueva_coop
                operador.save()

            return redirect("operador_list")

    else:
        form = OperadorEditForm(instance=user)

    cooperativas = Cooperativa.objects.all()

    return render(request, "administracion/operador_form.html", {
        "form": form,
        "operador": operador,
        "cooperativas": cooperativas,
        "editar": True
    })


@login_required
def operador_delete(request, pk):
    operador = get_object_or_404(Operador, pk=pk)

    if request.method == "POST":
        user = operador.user
        operador.delete()     # Borra Operador
        user.delete()         # Borra User relacionado
        return redirect("operador_list")

    return render(request, "administracion/operador_confirm_delete.html", {
        "operador": operador
    })
