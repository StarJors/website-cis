from django.shortcuts import render
from Gestion_Usuarios.models import models
from django.contrib.auth.models import Group
# Create your views here.

def prueba(request):
    grupos = Group.objects.all()
    return render(request, "prueba.html", {'grupos': grupos})