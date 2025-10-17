from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_admins(request):
    render(request, "home_admin.html")