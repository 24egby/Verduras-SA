from .models import Instalacion, Producto
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
import login.models as  LV

@login_required
def home_gerente(request):
    granjas = Instalacion.objects.filter(tipoInsta=1)
    bodegas = Instalacion.objects.filter(tipoInsta=2)
    admins = LV.UsuarioRol.objects.filter(idRol__in=[2, 3]).select_related('idInsta', 'idUserAuth')
    coords = LV.UsuarioRol.objects.filter(idRol__in=[3, 4]).select_related('idInsta', 'idUserAuth')
    productos = Producto.objects.all()
    context = {
        "admins": admins,
        "coords": coords,
        "granjas": granjas,
        "bodegas": bodegas,
        "productos": productos,
    }
    return render(request, "home_gerente.html", context)

#Area de gestion de Administradores
@login_required
def gestion_Admins(request):
    admins_Granjas = LV.UsuarioRol.objects.filter(idRol=2)
    admins_Bodegas = LV.UsuarioRol.objects.filter(idRol=3)
    context = {
        'admins_Granjas': admins_Granjas,
        'admins_Bodegas': admins_Bodegas
    }
    return render(request, "gestion_Administradores.html", context)


@login_required
@transaction.atomic
def crear_Admins(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        email = request.POST.get("email")
        password = request.POST.get("password")
        id_insta = request.POST.get("instalacion")  # ID de la instalación seleccionada
        try:
            if User.objects.filter(username=email).exists():
                messages.warning(request, "El correo ya está registrado.")
                return redirect("Agregar-Admin")

            user = User.objects.create_user(
                username=f"{nombre}.{apellido}",
                email=email,
                password=password,
                first_name=nombre,
                last_name=apellido,
            )

            # ✅ Obtener la instalación seleccionada
            instalacion = Instalacion.objects.get(id=id_insta)

            # ✅ Mapear tipoInsta → idRol
            if instalacion.tipoInsta == 1:
                id_rol = 2  # AdminGranja
                rol_texto = "Administrador de Granja"
            elif instalacion.tipoInsta == 2:
                id_rol = 3  # AdminBodega
                rol_texto = "Administrador de Bodega"
            else:
                id_rol = 2
                rol_texto = "Administrador (por defecto)"

            # ✅ Crear relación en UsuarioRol
            LV.UsuarioRol.objects.create(
                idUserAuth=user,
                idRol_id=id_rol,
                idInsta_id=id_insta
            )

            messages.success(
                request,
                f"{rol_texto} registrado exitosamente en '{instalacion.instalacion}'."
            )
            return redirect("Agregar-Admin")

        except Exception as e:
            print("Error al registrar:", e)
            messages.error(request, f"Ocurrió un error: {str(e)}")
            return redirect("Agregar-Admin")

    return render(request, "crear_Admins.html")

@login_required
def eliminar_admin(request, id_admin):
    if request.method == "POST":
        # Buscar el administrador en UsuarioRol
        admin = get_object_or_404(LV.UsuarioRol, id=id_admin)
        user_auth = admin.idUserAuth
        instalaciones = Instalacion.objects.filter(idAdmin=admin.id)
        for insta in instalaciones:
            insta.idAdmin = None
            insta.save()
        admin.delete()
        user_auth.delete()
        messages.success(request, "Administrador eliminado correctamente.")
        return redirect("Gestion-Admins")
    return redirect('Gestion-Admins') 


@login_required
def obtener_instalaciones(request):
    tipo = request.GET.get("tipo")
    if tipo:
        instalaciones = Instalacion.objects.filter(
            tipoInsta=tipo,
            idAdmin__isnull=True  
        ).values("id", "instalacion")
    else:
        instalaciones = Instalacion.objects.none()

    return JsonResponse(list(instalaciones), safe=False)


#Area de gestion de Granjas
@login_required
def gestion_Granjas(request):
    granjas = Instalacion.objects.filter(tipoInsta=1)
    admins_Granjas = LV.UsuarioRol.objects.filter(idRol=2).select_related('idUserAuth', 'idInsta')
    granjas_con_admin = []
    for g in granjas:
        admin = next((a for a in admins_Granjas if a.idInsta_id == g.id), None)
        g.admin = admin  # puede ser None si no hay admin
        granjas_con_admin.append(g)
    context = {
        "granjas": granjas_con_admin,
    }
    return render(request, "gestion_Granjas.html", context)

@login_required
def crear_Granja(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        dirrecion = request.POST.get('dirrecion')

        # Validación: campos vacíos
        if not nombre or not dirrecion:
            messages.error(request, "⚠️ Por favor complete todos los campos.")
            return redirect('Crear-Granja')

        # Normalizar texto para comparar sin mayúsculas o espacios
        nombre_limpio = nombre.strip().lower()
        dirrecion_limpia = dirrecion.strip().lower()

        # Validación: existencia previa
        if Instalacion.objects.filter(instalacion__iexact=nombre_limpio).exists():
            messages.error(request, "❌ Ya existe una granja con ese nombre.")
            return redirect('Crear-Granja')

        if Instalacion.objects.filter(dirrecion__iexact=dirrecion_limpia).exists():
            messages.error(request, "❌ Ya existe una granja con esa dirección.")
            return redirect('Crear-Granja')

        # Crear registro si todo es válido
        try:
            Instalacion.objects.create(
                instalacion=nombre,
                dirrecion=dirrecion,
                tipoInsta=1,  # Siempre 1 = Granja
                idAdmin=None,
                idCoord=None
            )
            messages.success(request, f"✅ La granja '{nombre}' fue registrada correctamente.")
        except Exception as e:
            messages.error(request, f"⚠️ Error al registrar: {e}")

        return redirect('Crear-Granja')

    return render(request, 'crear_Granja.html')

@login_required
@csrf_exempt
def eliminar_Granja(request, id):
    if request.method == 'POST':
        try:
            granja = Instalacion.objects.get(id=id)
            granja.delete()
            return JsonResponse({'success': True})
        except Instalacion.DoesNotExist:
            return JsonResponse({'error': 'Granja no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
   
   
#Vista Coordinadores 
@login_required 
def vista_coordinadores(request):
    coords_Granjas = LV.UsuarioRol.objects.filter(idRol_id=4)
    coords_Bodegas = LV.UsuarioRol.objects.filter(idRol_id=5)
    return render(request, "vista_Coord.html", {
        "coords_Granjas": coords_Granjas,
        "coords_Bodegas": coords_Bodegas,
    })
