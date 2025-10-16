"""
URL configuration for verduras_sa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

import login.views as VL
import gerente.views as VG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', VL.login_view, name="Login"),
    path("logout/", VL.logout_g, name="logout"),
    
    #Rutas Gerente
    path('Gerente', VG.home_gerente, name="Gerente"),
    
    #Gestion Granjas
    path('Gerente/Gestion-Granjas', VG.gestion_Granjas, name="Gestion-Granjas"),
    path('Gerente/Gestion-Granjas/Crear-Granja', VG.crear_Granja, name="Crear-Granja"),
    path('Gerente/Gestion-Granjas/Eliminar-Granja/<int:id>/', VG.eliminar_Granja, name='Eliminar-Granja'),
    #Gestion Admins
    path('Gerente/Gestion-Admin', VG.gestion_Admins, name="Gestion-Admins"),
    path('Gerente/Gestion-Admin/Agregar-Admin', VG.crear_Admins, name="Agregar-Admin"),
    path('Gerente/Gestion-Admin/Obtener-Instalaciones/', VG.obtener_instalaciones, name='Obtener-Instalaciones'),
    path('Gerente/Gestion-Admin/Eliminar-Admin/<int:id_admin>/', VG.eliminar_admin, name="Eliminar-Admin"),
    #Vista Coords
    path('Gerente/Vista-Coords', VG.vista_coordinadores, name="Vista-Coords"),
    
    
    
    
    
    
    
    
    #Rutas Admin Granja
    #path('Admin-Granja', VL.home_adminGranja, name="Admin-Granja"),
    
    #Rutas Admin Bodega
    #path('Admin-Bodega', VL.home_adminBodega, name="Admin-Bodega"),
    
    #Rutas Coor Granja
    #path('Coor-Granja', VL.home_coorGranja, name="Coord-Granja"),
    
    #Rutas Coor Bodega
    #path('Coord-Bodega', VL.home_coorBodega, name="Coord-Bodega"),
    
    #Rutas Empleado Bodega
    #path('Emple-Bodega', VL.home_empleado, name="Emple-Bodega"),
]
