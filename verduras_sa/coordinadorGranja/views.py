from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_coord_granja(request):
    render(request, "home_coordinador_granja.html")