from django.urls import path
from . import views

urlpatterns = [

    # -----------------------------
    # LOGIN / LOGOUT
    # -----------------------------
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # -----------------------------
    # HOME GENERAL
    # -----------------------------
    path('', views.panel_home, name='panel_home'),
    path('usuario/', views.usuario_home, name='usuario_home'),

    # -----------------------------
    # VISTAS ANTIGUAS (MVC)
    # -----------------------------
    path('cooperativas/', views.CooperativaListView.as_view(), name='cooperativa_list'),
    path('cooperativas/nuevo/', views.CooperativaCreateView.as_view(), name='cooperativa_create'),

    path('buses/', views.BusListView.as_view(), name='bus_list'),
    path('buses/nuevo/', views.BusCreateView.as_view(), name='bus_create'),

    path('reservas/', views.ReservaListView.as_view(), name='reserva_list'),
    path('reservas/nuevo/', views.ReservaCreateView.as_view(), name='reserva_create'),

    path('api/buses/', views.buses_por_cooperativa, name='api_buses_por_cooperativa'),

    path('monitoreo/', views.MonitoreoView.as_view(), name='monitoreo'),

    # =============================
    # PANEL SUPERADMIN (NUEVO)
    # =============================
    path('panel/', views.panel_admin, name='panel_admin'),

    # CRUD COOPERATIVAS (Panel)
    path('panel/cooperativas/', views.cooperativa_list, name='super_cooperativa_list'),
    path('panel/cooperativas/nueva/', views.cooperativa_create, name='super_cooperativa_create'),
    path('panel/cooperativas/<int:pk>/editar/', views.cooperativa_edit, name='super_cooperativa_edit'),
    path('panel/cooperativas/<int:pk>/eliminar/', views.cooperativa_delete, name='super_cooperativa_delete'),

    # CRUD BUSES (Panel)
    path('panel/buses/', views.bus_list, name='super_bus_list'),
    path('panel/buses/nuevo/', views.bus_create, name='super_bus_create'),
    path('panel/buses/<int:pk>/editar/', views.bus_edit, name='super_bus_edit'),
    path('panel/buses/<int:pk>/eliminar/', views.bus_delete, name='super_bus_delete'),

    # CRUD RUTAS (Panel)
    path('panel/rutas/', views.ruta_list, name='super_ruta_list'),
    path('panel/rutas/nueva/', views.ruta_create, name='super_ruta_create'),
    path('panel/rutas/<int:pk>/editar/', views.ruta_edit, name='super_ruta_edit'),
    path('panel/rutas/<int:pk>/eliminar/', views.ruta_delete, name='super_ruta_delete'),

    # CRUD HORARIOS (Panel)
    path('panel/horarios/', views.horario_list, name='super_horario_list'),
    path('panel/horarios/nuevo/', views.horario_create, name='super_horario_create'),
    path('panel/horarios/<int:pk>/editar/', views.horario_edit, name='super_horario_edit'),
    path('panel/horarios/<int:pk>/eliminar/', views.horario_delete, name='super_horario_delete'),

    # CRUD OPERADORES (Panel)
    path('panel/operadores/', views.operador_list, name='operador_list'),
    path('panel/operadores/nuevo/', views.operador_create, name='operador_create'),
    
    # CRUD OPERADORES
    path('panel/operadores/', views.operador_list, name='operador_list'),
    path('panel/operadores/nuevo/', views.operador_create, name='operador_create'),
    path('panel/operadores/<int:pk>/editar/', views.operador_edit, name='operador_edit'),
    path('panel/operadores/<int:pk>/eliminar/', views.operador_delete, name='operador_delete'),



]
