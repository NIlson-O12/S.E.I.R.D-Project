from django import forms
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.apps import apps


Usuario = get_user_model()

class ParametrosSimulacionForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('simuladorApp', 'ParametrosSimulacion')
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
            self.add_error("poblacionInicial", "La población inicial debe ser mayor que cero.")

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


class RegistroEstudianteForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "********"})
    )
    password2 = forms.CharField(
        label="Confirmar contraseña", 
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "********"})
    )

    class Meta:
        model = Usuario  
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre"}),
            'last_name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellido"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "placeholder": "ejemplo@correo.com"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
            
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.username = self.cleaned_data["email"]  
        usuario.set_password(self.cleaned_data["password1"])
        usuario.rol = 'estudiante'  
        
        if commit:
            usuario.save()
        return usuario


class LoginEstudianteForm(forms.Form):
    email = forms.EmailField( 
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={  
            "class": "form-control",
            "placeholder": "ejemplo@correo.com",
            "style": "min-width: 300px; padding: 10px;" 
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "********",
            "style": "min-width: 300px; padding: 10px;" 
        })
    )
