"""
URL configuration for lasinuana project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from main.views import *
from .views import *
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from . import views

urlpatterns = [
    path('',login, name="login"),
    path('dashboard/',dashboard,name="dashboard"),
    path('registro/', registro_usuario, name='registro_usuario'),
    path('registroempleado/', registrar_empleado, name='registrar_empleado'),
    path('crear/', crear_empleado, name='crear_empleado'),
    path('obtener_empleado/<int:empleado_id>/', views.obtener_empleado, name='obtener_empleado'),
    path('user_information/', user_information, name='user_information'),
    path('guardar-cambios-usuario/', guardar_cambios_usuario, name='guardar_cambios_usuario'),
    path('logout/', logout_view, name='logout'),
    path('empleados/', views.empleados, name='empleados'),
    path('registrar-asistencia/', views.registrar_asistencia, name='registrar_asistencia'),
    path('solicitudes/', views.solicitudes, name='solicitudes'),
    path('calendario/', views.calendario, name='calendario'),
    path('ejemplo/', views.ejemplo, name='ejemplo'),
    path('capacitacion/ges_formacion/', views.ges_formacion, name='ges_formacion'),
    path('planes_formacion/', views.vista_planes_formacion, name="planes_formacion"),
    path('capacitacion/inscripciones/', views.inscripciones, name='inscripciones'),
    path('obtener_empleados/', views.obtener_sugerencias_empleados, name='obtener_empleados'),
    path('capacitacion/registro_cer/', views.registro_cer, name='registro_cer'),
    path('seguridad/ges_usuario/', views.ges_usuario, name='ges_usuario'),
    path('seguridad/control_acceso/', views.control_acceso, name='control_acceso'),

    

]
