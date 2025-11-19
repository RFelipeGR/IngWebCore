from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# -----------------------------------
# LISTA DE CIUDADES (DEBE IR ARRIBA)
# -----------------------------------
CIUDADES = [
    # --- SIERRA NORTE ---
    ("Quito", "Quito"),
    ("Cayambe", "Cayambe"),
    ("Ibarra", "Ibarra"),
    ("Otavalo", "Otavalo"),
    ("Tulcán", "Tulcán"),

    # --- SIERRA CENTRO ---
    ("Latacunga", "Latacunga"),
    ("Ambato", "Ambato"),
    ("Salcedo", "Salcedo"),
    ("Riobamba", "Riobamba"),
    ("Guaranda", "Guaranda"),
    ("Baños", "Baños"),

    # --- SIERRA SUR ---
    ("Cuenca", "Cuenca"),
    ("Azogues", "Azogues"),
    ("Cañar", "Cañar"),
    ("Loja", "Loja"),
    ("Zamora", "Zamora"),
    ("Macas", "Macas"),

    # --- COSTA NORTE ---
    ("Esmeraldas", "Esmeraldas"),
    ("Atacames", "Atacames"),
    ("Santo Domingo", "Santo Domingo"),
    ("Quinindé", "Quinindé"),

    # --- COSTA CENTRO ---
    ("Manabí", "Portoviejo"),
    ("Manta", "Manta"),
    ("Chone", "Chone"),
    ("El Carmen", "El Carmen"),

    # --- COSTA SUR ---
    ("Guayaquil", "Guayaquil"),
    ("Milagro", "Milagro"),
    ("Babahoyo", "Babahoyo"),
    ("Quevedo", "Quevedo"),
    ("Machala", "Machala"),
    ("Pasaje", "Pasaje"),
    ("Huaquillas", "Huaquillas"),
    ("Santa Rosa", "Santa Rosa"),

    # --- ORIENTE ---
    ("Tena", "Tena"),
    ("Puyo", "Puyo"),
    ("El Coca", "El Coca"),
    ("Lago Agrio", "Lago Agrio"),
    ("Sucumbíos", "Sucumbíos"),

    # --- GALÁPAGOS (POCO USADA PERO FORMALMENTE VÁLIDA) ---
    ("San Cristóbal", "San Cristóbal"),
    ("Santa Cruz", "Santa Cruz"),
]
    
class Cooperativa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    ruc = models.CharField(max_length=13, unique=True)
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    def clean(self):
        if not self.ruc.isdigit() or len(self.ruc) != 13:
            raise ValidationError("El RUC debe tener exactamente 13 dígitos numéricos.")

        if self.telefono and not self.telefono.isdigit():
            raise ValidationError("El teléfono debe contener solo números.")

    def __str__(self):
        return f"{self.nombre} ({self.ruc})"


class Operador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cooperativa = models.ForeignKey(Cooperativa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} ({self.cooperativa.nombre})"


class Bus(models.Model):
    cooperativa = models.ForeignKey(Cooperativa, on_delete=models.CASCADE)
    placa = models.CharField(max_length=20)
    capacidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.placa} - {self.cooperativa.nombre}"


# -----------------------------------
# AQUÍ USAMOS LA LISTA CIUDADES
# -----------------------------------
class Ruta(models.Model):
    origen = models.CharField(max_length=100, choices=CIUDADES)
    destino = models.CharField(max_length=100, choices=CIUDADES)

    def __str__(self):
        return f"{self.origen} → {self.destino}"


class Horario(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    hora_salida = models.DateTimeField()

    def __str__(self):
        return f"{self.ruta} - {self.hora_salida} - {self.bus.placa}"
