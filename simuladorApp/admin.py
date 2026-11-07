from django.contrib import admin
from .models import ParametrosSimulacion


@admin.register(ParametrosSimulacion)
class ParametrosSimulacionAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "fecha_creacion", "poblacionInicial", "infectadosInicial", "tiempoSimulacion")
    list_filter = ("fecha_creacion",)
    search_fields = ("usuario__username",)
    readonly_fields = ("fecha_creacion",)
