from django.shortcuts import render #, redirect, get_object_or_404
from django.contrib.auth import get_user_model
#from django.core.paginator import Paginator
#from django.db.models import Q
from .models import Titulado
User = get_user_model()

# Create your views here.
def lista_titulados(request):
    titulados = Titulado.objects.all()
    return render(request, 'lista_titulados.html', {'titulados': titulados})
