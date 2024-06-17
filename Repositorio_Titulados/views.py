from django.shortcuts import render #, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q

User = get_user_model()

# Create your views here.
def listar_titulados(request):
    titulados = User.objects.all()
    return render(request, 'listar_titulados.html', {'titulados': titulados})
