from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, CreateView

from .forms import ReservaForm, LoginForm
from .models import Cooperativa, Bus, Ruta, Reserva

from django.db.models import Count, F, FloatField, ExpressionWrapper

from django.contrib.auth import logout


# ======================
#   LOGOUT
# ======================
def logout_view(request):
    logout(request)
    return redirect('/panel/login/')



# ======================
#   MIXIN PARA ADMIN
# ======================
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


# ======================
#   LOGIN
# ======================

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():  # VALIDACIÓN BACKEND
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                if user.is_staff:
                    return redirect('/panel/')          # PANEL ADMIN
                else:
                    return redirect('/panel/usuario/')  # PANEL USUARIO

            else:
                form.add_error(None, "Credenciales incorrectas")

    else:
        form = LoginForm()

    return render(request, 'administracion/login.html', {'form': form})


# ======================
#   PANEL HOME (ADMIN)
# ======================

def panel_home(request):
    return render(request, 'administracion/panel_home.html')


# ======================
#   PANEL HOME (USUARIO)
# ======================

def usuario_home(request):
    return render(request, 'administracion/usuario_home.html')


# ======================
#   CRUD COOPERATIVA
# ======================

class CooperativaListView(AdminRequiredMixin, ListView):
    model = Cooperativa
    template_name = 'administracion/cooperativa_list.html'


class CooperativaCreateView(AdminRequiredMixin, CreateView):
    model = Cooperativa
    fields = [
        'nombre', 'ruc', 'correo', 'telefono',
        'umbral_ocupacion', 'porcentaje_comision',
        'ventana_inicio', 'ventana_fin'
    ]
    template_name = 'administracion/cooperativa_form.html'
    success_url = reverse_lazy('cooperativa_list')


# ======================
#   CRUD BUS
# ======================

class BusListView(AdminRequiredMixin, ListView):
    model = Bus
    template_name = 'administracion/bus_list.html'


class BusCreateView(AdminRequiredMixin, CreateView):
    model = Bus
    fields = ['cooperativa', 'placa', 'capacidad']
    template_name = 'administracion/bus_form.html'
    success_url = reverse_lazy('bus_list')


# ======================
#   RESERVAS (USUARIO y ADMIN)
# ======================

class ReservaListView(ListView):
    model = Reserva
    template_name = 'administracion/reserva_list.html'


class ReservaCreateView(CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'administracion/reserva_form.html'
    success_url = reverse_lazy('reserva_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cooperativas'] = Cooperativa.objects.all()
        return context


# ======================
#   API BUSES (DROPDOWN)
# ======================

def buses_por_cooperativa(request):
    cooperativa_id = request.GET.get('cooperativa_id')
    data = []

    if cooperativa_id:
        buses = Bus.objects.filter(cooperativa_id=cooperativa_id).order_by('placa')
        data = [
            {'id': bus.id, 'texto': f"{bus.placa} (cap: {bus.capacidad})"}
            for bus in buses
        ]

    return JsonResponse({'buses': data})


# ======================
#   MONITOREO (ADMIN)
# ======================

class MonitoreoView(AdminRequiredMixin, ListView):
    model = Bus
    template_name = 'administracion/monitoreo.html'

    def get_queryset(self):
        return Bus.objects.annotate(
            reservas_count=Count('reservas'),
            ocupacion=ExpressionWrapper(
                100.0 * Count('reservas') / F('capacidad'),
                output_field=FloatField()
            )
        )
