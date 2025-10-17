from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto

@login_required
def home_empleado(request):
    productos = Producto.objects.all()  # Obtiene todos los productos de la BD
    if request.method == "POST":
        producto_id = request.POST.get("producto")
        estado = request.POST.get("estado")
        cantidad = request.POST.get("cantidad")

        # Aquí podrías guardar la clasificación o hacer otra lógica
        # ...

        return redirect("Empleado-Bodega")  # Recarga la página después de guardar

    return render(request, "home_Empleado.html", {"productos": productos})