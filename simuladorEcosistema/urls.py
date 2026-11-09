from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from simuladorApp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.simulador, name="simulator"),
    
    path("login/", views.login_usuario, name="login"),
    
    path("registration/", views.registro, name="registration"),
    path("cerrar_sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path('alternar-tema/', views.alternar_tema, name='alternar_tema'),
    path("configuration/", views.configuracion, name="configuration"),
    path('panel_profesor/', views.panel_profesor, name='panel_profesor'),
    path('panel_profesor/historial/', views.historial_simulaciones, name='historial_simulaciones'),
    path('panel_profesor/escenario/crear/', views.crear_escenario, name='crear_escenario'),
    path('panel_profesor/escenario/editar/<int:id>/', views.editar_escenario, name='editar_escenario'),
    path('panel_profesor/escenario/eliminar/<int:id>/', views.eliminar_escenario, name='eliminar_escenario'),
    
]
