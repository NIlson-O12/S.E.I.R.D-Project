from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


# Tabla de simulacion
class ParametrosSimulacion(models.Model):
    """Parámetros y registro histórico de cada simulación ejecutada."""
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="simulaciones",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tasaInfeccion = models.FloatField()
    tasaRecuperacion = models.FloatField()
    tasaMortalidad = models.FloatField()
    duracionPromedioEnfermedad = models.IntegerField()  # en días
    poblacionInicial = models.IntegerField()
    infectadosInicial = models.IntegerField()
    tiempoSimulacion = models.IntegerField()

    class Meta:
        ordering = ["-fecha_creacion"]
        verbose_name = "Simulación"
        verbose_name_plural = "Simulaciones"

    def __str__(self):
        return f"Simulación #{self.pk} - {self.fecha_creacion:%Y-%m-%d %H:%M}"
    

class Usuario(AbstractUser):
    ROLE_CHOICES = (
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=15, choices=ROLE_CHOICES, default='estudiante')
    telefono = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"



class PerfilProfesor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_profesor')
    especialidad = models.CharField(max_length=100)
    cubiculo = models.CharField(max_length=10, blank=True, null=True)

class PerfilEstudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_estudiante')
    matricula = models.CharField(max_length=20, unique=True)
    carrera = models.CharField(max_length=100)
