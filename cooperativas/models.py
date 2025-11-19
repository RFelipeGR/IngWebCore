# cooperativas/models.py
from django.db import models
from django.contrib.auth.models import User

class Cooperativa(models.Model):
    nombre = models.CharField(max_length=100)
    # más campos si quieres (RUC, dirección, etc.)

    def __str__(self):
        return self.nombre

class Operador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cooperativa = models.ForeignKey(Cooperativa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} ({self.cooperativa.nombre})"
