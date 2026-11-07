from django.conf import settings
from django.db import models


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
# Tabla de gestion de cuentas

# Tabla de informacion guardada