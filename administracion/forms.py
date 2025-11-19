from django import forms
from django.contrib.auth.models import User
from .models import Cooperativa, Bus, Ruta, Horario, Operador


class CooperativaForm(forms.ModelForm):
    class Meta:
        model = Cooperativa
        fields = ['nombre', 'ruc', 'direccion', 'telefono', 'email']


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['cooperativa', 'placa', 'capacidad']


class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = ['origen', 'destino']


class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['bus', 'ruta', 'hora_salida']

    def save(self, commit=True):
        horario = super().save(commit=False)
        horario.capacidad_total = horario.bus.capacidad
        if commit:
            horario.save()
        return horario


class OperadorCreateForm(forms.Form):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    cooperativa = forms.ModelChoiceField(queryset=Cooperativa.objects.all())

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ese nombre de usuario ya existe.")
        return username

    def save(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password1"]
        cooperativa = self.cleaned_data["cooperativa"]

        user = User.objects.create_user(
            username=username,
            password=password,
            is_staff=False,
            is_superuser=False
        )

        operador = Operador.objects.create(
            user=user,
            cooperativa=cooperativa
        )

        return user, operador


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingresa tu usuario',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingresa tu contraseña',
            'class': 'form-control'
        })
    )


# =====================================================
#   FORMULARIO CORRECTO PARA EDITAR OPERADOR
# =====================================================
class OperadorEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Ese nombre de usuario ya existe.")
        return username
