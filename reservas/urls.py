from django.urls import path
from . import views

urlpatterns = [
    # Panel del operador
    path('panel/', views.panel_operador, name='panel_operador'),

    # Detalle de una reserva según el ID de Horario o Reserva
    path('reserva/<int:id>/', views.detalle_reserva, name='detalle_reserva'),

    # Transferencias basadas en CORE
    path('reserva/<int:id>/transferencias/', views.transferencias, name='transferencias'),

    # Estadísticas del horario
    path('reserva/<int:id>/estadisticas/', views.estadisticas_reserva, name='estadisticas_reserva'),
    
        # 🔥 NUEVO
    path('logout/', views.operador_logout, name='operador_logout'),
]
