from django.contrib import admin
from .models import ParametrosSimulacion
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, PerfilProfesor, PerfilEstudiante


@admin.register(ParametrosSimulacion)
class ParametrosSimulacionAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "fecha_creacion", "poblacionInicial", "infectadosInicial", "tiempoSimulacion")
    list_filter = ("fecha_creacion",)
    search_fields = ("usuario__username",)
    readonly_fields = ("fecha_creacion",)

class PerfilProfesorInline(admin.StackedInline):
    model = PerfilProfesor
    can_delete = False
    verbose_name_plural = 'Perfil de Profesor'

class PerfilEstudianteInline(admin.StackedInline):
    model = PerfilEstudiante
    can_delete = False
    verbose_name_plural = 'Perfil de Estudiante'

class PersonalizadoUserAdmin(UserAdmin):
    inlines = (PerfilProfesorInline, PerfilEstudianteInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff')
    list_filter = ('rol', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Rol', {'fields': ('rol', 'telefono')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información de Rol', {'fields': ('rol', 'telefono')}),
    )

admin.site.register(Usuario, PersonalizadoUserAdmin)
