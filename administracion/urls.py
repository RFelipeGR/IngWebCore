from django.urls import path
from .views import (
    CooperativaListView, CooperativaCreateView,
    BusListView, BusCreateView,
    ReservaListView, ReservaCreateView,
    buses_por_cooperativa, login_view, logout_view, panel_home, usuario_home
)
from .views import MonitoreoView


urlpatterns = [
    path('login/', login_view, name='login'),
    path('usuario/', usuario_home, name='usuario_home'),
    path('', panel_home, name='panel_home'),
    path('logout/', logout_view, name='logout'),


    
    path('cooperativas/', CooperativaListView.as_view(), name='cooperativa_list'),
    path('cooperativas/nuevo/', CooperativaCreateView.as_view(), name='cooperativa_create'),

    path('buses/', BusListView.as_view(), name='bus_list'),
    path('buses/nuevo/', BusCreateView.as_view(), name='bus_create'),

    path('reservas/', ReservaListView.as_view(), name='reserva_list'),
    path('reservas/nuevo/', ReservaCreateView.as_view(), name='reserva_create'),

    path('api/buses/', buses_por_cooperativa, name='api_buses_por_cooperativa'),

    # NUEVO
    path('monitoreo/', MonitoreoView.as_view(), name='monitoreo'),
]
