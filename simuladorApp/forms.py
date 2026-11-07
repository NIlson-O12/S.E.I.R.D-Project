from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ParametrosSimulacion


class ParametrosSimulacionForm(forms.ModelForm):
    class Meta:
        model = ParametrosSimulacion
        fields = [
            "tasaInfeccion",
            "tasaRecuperacion",
            "tasaMortalidad",
            "duracionPromedioEnfermedad",
            "poblacionInicial",
            "infectadosInicial",
            "tiempoSimulacion",
        ]
        labels = {
            "tasaInfeccion": "Tasa de infección",
            "tasaRecuperacion": "Tasa de recuperación",
            "tasaMortalidad": "Tasa de mortalidad",
            "duracionPromedioEnfermedad": "Duración promedio de la enfermedad",
            "poblacionInicial": "Población inicial",
            "infectadosInicial": "Infectados iniciales",
            "tiempoSimulacion": "Tiempo de simulación",
        }
        widgets = {
            "tasaInfeccion": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0", "max": "1"}),
            "tasaRecuperacion": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0", "max": "1"}),
            "tasaMortalidad": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0", "max": "1"}),
            "duracionPromedioEnfermedad": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "poblacionInicial": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "infectadosInicial": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "tiempoSimulacion": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
        }



    def _validar_tasa(self, campo, etiqueta):
        tasa = self.cleaned_data.get(campo)
        if tasa is None:
            return tasa
        if not 0 <= tasa <= 1:
            raise forms.ValidationError(f"La {etiqueta} debe estar entre 0 y 1.")
        return tasa

    def clean_tasaInfeccion(self):
        return self._validar_tasa("tasaInfeccion", "tasa de infección")

    def clean_tasaRecuperacion(self):
        return self._validar_tasa("tasaRecuperacion", "tasa de recuperación")

    def clean_tasaMortalidad(self):
        return self._validar_tasa("tasaMortalidad", "tasa de mortalidad")

    def clean(self):
        cleaned_data = super().clean()
        poblacion = cleaned_data.get("poblacionInicial")
        infectados = cleaned_data.get("infectadosInicial")
        duracion = cleaned_data.get("duracionPromedioEnfermedad")
        dias = cleaned_data.get("tiempoSimulacion")

        if poblacion is not None and poblacion <= 0:
            self.add_error("poblacion Inicial", "La población inicial debe ser mayor que cero.")

        if infectados is not None and infectados <= 0:
            self.add_error("infectadosInicial", "Los infectados iniciales deben ser mayores que cero.")

        if (
            poblacion is not None
            and infectados is not None
            and infectados >= poblacion
        ):
            self.add_error(
                "infectadosInicial",
                "El número de infectados iniciales debe ser menor que la población inicial.",
            )

        if duracion is not None and duracion <= 0:
            self.add_error(
                "duracionPromedioEnfermedad",
                "La duración promedio de enfermedad debe ser mayor que cero.",
            )
        if dias is not None and not 1 <= dias <= 3650:
            self.add_error("tiempoSimulacion", "La simulación debe durar entre 1 y 3650 días.")

        return cleaned_data


    """El registro público crea únicamente cuentas de estudiante."""
class RegistroEstudianteForm(forms.Form):
    name = forms.CharField(
        max_length=150, 
        label="Nombre", 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre"})
    )
    lastname = forms.CharField(
        max_length=150, 
        label="Apellido", 
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellido"})
    )
    email = forms.EmailField(
        label="Correo electrónico", 
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "ejemplo@correo.com"})
    )
    password1 = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "********"})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña", 
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "********"})
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
            
        return cleaned_data

class LoginEstudianteForm(forms.Form):
    email = forms.EmailField( 
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={  
            "class": "form-control; align-items: center; ",
            "placeholder": "ejemplo@correo.com",
            "style": "width: 50px; min-width: 300px; padding: 10px;" 
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control; align-items: center; ",
            "placeholder": "********",
            "style": "width: 50px; min-width: 300px; padding: 10px;" 
        })
    )




