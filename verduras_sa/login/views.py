from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import UsuarioRol
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                usuario_rol = UsuarioRol.objects.get(idUserAuth=user.id)
                rol_nombre = usuario_rol.idRol.rol
            except UsuarioRol.DoesNotExist:
                error = "No tienes un rol asignado."
                return redirect("Login")
            # Redirección según el rol
            if rol_nombre == "Gerente":
                return redirect("Gerente")
            elif rol_nombre == "AdminGranja":
                return redirect("Admin-Granja")
            elif rol_nombre == "AdminBodega":
                return redirect("Admin-Bodega")
            elif rol_nombre == "CoorGranja":
                return redirect("Coord-Granja")
            elif rol_nombre == "CoordBodega":
                return redirect("Coord-Bodega")
            elif rol_nombre == "EmpleBodega":
                return redirect("Emple-Bodega")
        else:
            error = "Usuario o contraseña incorrectos."
    return render(request, "index.html", {'error': error})

@login_required
def logout_g(request):
    logout(request)
    return redirect("Login")