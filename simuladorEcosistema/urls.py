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
]
