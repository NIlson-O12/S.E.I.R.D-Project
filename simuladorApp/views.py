import base64
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from django.utils.text import slugify
import uuid  


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from .forms import ParametrosSimulacionForm, RegistroEstudianteForm, LoginEstudianteForm
from .utilis import simular_seir


def simulador(request):
    if not request.user.is_authenticated:
        return redirect("login")
        
    tema_actual = request.session.get('theme', 'light')
    es_oscuro = (tema_actual == 'dark')
        
    if request.method == "POST":
        form = ParametrosSimulacionForm(request.POST)
        if form.is_valid():
            tasa_infeccion = form.cleaned_data["tasaInfeccion"]
            tasa_recuperacion = form.cleaned_data["tasaRecuperacion"]
            tasa_mortalidad = form.cleaned_data["tasaMortalidad"]
            duracion_enfermedad = form.cleaned_data["duracionPromedioEnfermedad"]
            poblacion_inicial = form.cleaned_data["poblacionInicial"]
            infectados_inicial = form.cleaned_data["infectadosInicial"]
            tiempo_simulacion = form.cleaned_data["tiempoSimulacion"]
            
            tasa_incubacion = min(1 / duracion_enfermedad, 1)
            s0 = poblacion_inicial - infectados_inicial
            e0 = 0
            i0 = infectados_inicial
            r0 = 0
            d0 = 0
            
            S, E, I, R, D = simular_seir(
                tasa_infeccion=tasa_infeccion, tasa_incubacion=tasa_incubacion,
                tasa_recuperacion=tasa_recuperacion, tasa_mortalidad=tasa_mortalidad,
                S0=s0, E0=e0, I0=i0, R0=r0, D0=d0, dias=tiempo_simulacion,
            )
            
            recomendaciones = []
            if np.max(I) > poblacion_inicial * 0.2:
                recomendaciones.append("Implementar cuarentenas focalizadas para reducir la propagación.")
            if np.max(I) > 100:
                recomendaciones.append("Incrementar campañas de vacunación y diagnóstico temprano.")
            if tiempo_simulacion > 30:
                recomendaciones.append("Promover medidas de protección personal en espacios cerrados.")
            if I[-1] > I[0] * 1.5:
                recomendaciones.append("Reducir movilidad en zonas de alto contagio.")
            if np.max(R) < poblacion_inicial * 0.1:
                recomendaciones.append("Fortalecer la capacidad hospitalaria y protocolos de tratamiento.")
            if not recomendaciones:
                recomendaciones.append("El escenario es estable; mantener monitoreo y vigilancia epidemiológica.")
            
            plt.figure(figsize=(10, 5))
            
            if es_oscuro:
                plt.style.use('dark_background')
                color_bg = "#1e1e1e" 
                color_texto = "#ffffff"
                color_s, color_e, color_i, color_r, color_d = "#3b82f6", "#f59e0b", "#ef4444", "#10b981", "#a3a3a3"
            else:
                plt.style.use('default')
                color_bg = "#ffffff"
                color_texto = "#000000"
                color_s, color_e, color_i, color_r, color_d = "blue", "orange", "red", "green", "black"

            dias = range(tiempo_simulacion + 1)
            plt.plot(dias, S, label="Susceptibles", color=color_s)
            plt.plot(dias, E, label="Expuestos", color=color_e)
            plt.plot(dias, I, label="Infectados", color=color_i)
            plt.plot(dias, R, label="Recuperados", color=color_r)
            plt.plot(dias, D, label="Fallecidos", color=color_d)
            
            plt.xlabel("Días", color=color_texto)
            plt.ylabel("Población", color=color_texto)
            plt.title("Simulación epidemiológica (SEIRD)", color=color_texto)
            
            plt.legend(facecolor=color_bg, edgecolor=color_texto)
            plt.tight_layout()
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format="png", facecolor=color_bg, edgecolor='none')
            plt.close()
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            buffer.close()
            
            tiempo_pico = int(np.argmax(I))
            porcentaje_infectados = round((float(np.max(I)) / poblacion_inicial) * 100, 2)
            porcentaje_recuperados = round((float(np.max(R)) / poblacion_inicial) * 100, 2)
            
            return render(
                request,
                "simuladorApp/results.html",
                {
                    "grafico": image_base64,
                    "recomendaciones": recomendaciones,
                    "tiempo_pico": tiempo_pico,
                    "porcentaje_infectados": porcentaje_infectados,
                    "porcentaje_recuperados": porcentaje_recuperados,
                },
            )
    else:
        form = ParametrosSimulacionForm()
    return render(request, "simuladorApp/simulator.html", {"form": form})

def alternar_tema(request):
    tema_actual = request.session.get('theme', 'light')
    request.session['theme'] = 'dark' if tema_actual == 'light' else 'light'
    return redirect(request.META.get('HTTP_REFERER', 'simulator'))


def registro(request):
    if request.user.is_authenticated:
        return redirect("simulator")
        
    if request.method == "POST":
        form = RegistroEstudianteForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data.get("email")
                nombre = form.cleaned_data.get("name")      
                apellido = form.cleaned_data.get("lastname")  
                password = form.cleaned_data.get("password11" if "password11" in form.cleaned_data else "password1")
                
                base_username = f"{slugify(nombre)} {slugify(apellido)}".lower()[:140]
                username_propuesto = base_username
                
                contador = 1
                while User.objects.filter(username=username_propuesto).exists():
                    username_propuesto = f"{base_username}{contador}"
                    contador += 1
                
                user = User.objects.create_user(
                    username=username_propuesto, 
                    email=email, 
                    password=password,
                    first_name=nombre,    
                    last_name=apellido   
                )
                login(request, user)
                
                messages.success(request, "Cuenta creada correctamente. Bienvenido/a.")
                return redirect("simulator")
            except Exception as e:
                messages.error(request, f"Error al registrar en el sistema: {str(e)}")
    else:
        form = RegistroEstudianteForm()
    return render(request, "simuladorApp/registration.html", {"form": form})


def login_usuario(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Profesores').exists():
            return redirect("panel_profesor")  
        return redirect("simulator")
        
    if request.method == "POST":
        form = LoginEstudianteForm(request.POST)
        if form.is_valid():
            correo_ingresado = form.cleaned_data.get('email')
            password_usuario = form.cleaned_data.get('password')
            
            try:
                usuario_objeto = User.objects.get(email__iexact=correo_ingresado)
                
                if usuario_objeto.check_password(password_usuario):
                    if usuario_objeto.is_active:
                        login(request, usuario_objeto)
                        
                        # --- CLAVE: Redirección según el Rol/Grupo ---
                        if usuario_objeto.groups.filter(name='Profesores').exists():
                            return redirect("simulator") 
                        else:
                            return redirect("simulator") 
                        
                    else:
                        form.add_error(None, "Esta cuenta se encuentra inactiva.")
                else:
                    form.add_error(None, "El correo electrónico o la contraseña son incorrectos.")
                    
            except User.DoesNotExist:
                form.add_error(None, "El correo electrónico o la contraseña son incorrectos.")
    else:
        form = LoginEstudianteForm()
        
    return render(request, "simuladorApp/login.html", {"form": form})



def cerrar_sesion(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("simulator")
