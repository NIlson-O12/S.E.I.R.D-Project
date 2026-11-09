from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

Usuario = get_user_model()

def rol_requerido(*roles):
    def decorador(vista):
        @login_required
        @wraps(vista)
        def protegida(request, *args, **kwargs):
            if request.user.rol not in roles:
                raise PermissionDenied("No tienes permisos para acceder a esta sección.")
            return vista(request, *args, **kwargs)
        return protegida
    return decorador

def es_profesor(usuario):
    return usuario.is_authenticated and usuario.rol == 'profesor'

def es_estudiante(usuario):
    return usuario.is_authenticated and usuario.rol == 'estudiante'
