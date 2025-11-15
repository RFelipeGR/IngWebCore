from django import forms
from .models import Reserva, Bus
from django import forms



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['bus', 'pasajero_nombre', 'pasajero_cedula', 'fecha_viaje', 'asiento']

    def clean_pasajero_cedula(self):
        cedula = self.cleaned_data.get('pasajero_cedula')

        # Validación básica: 10 dígitos numéricos
        if not cedula.isdigit():
            raise forms.ValidationError("La cédula solo debe contener números.")
        if len(cedula) != 10:
            raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos.")

        # Aquí podrías implementar el algoritmo de cédula ecuatoriana si quieres más nivel.

        return cedula

    def clean(self):
        cleaned_data = super().clean()
        bus = cleaned_data.get('bus')
        asiento = cleaned_data.get('asiento')
        fecha_viaje = cleaned_data.get('fecha_viaje')

        if bus and asiento and fecha_viaje:
            # Evitar doble reserva del mismo asiento en el mismo bus y fecha
            existe = Reserva.objects.filter(
                bus=bus,
                asiento=asiento,
                fecha_viaje=fecha_viaje
            ).exists()
            if existe:
                raise forms.ValidationError(
                    f"El asiento {asiento} ya está reservado para ese bus y fecha."
                )

            # Validar que el asiento no supere la capacidad
            if asiento > bus.capacidad:
                raise forms.ValidationError(
                    f"El asiento {asiento} supera la capacidad del bus ({bus.capacidad})."
                )
        return cleaned_data
