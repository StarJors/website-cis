from Gestion_Usuarios.models import models
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect , HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.views import View
from .forms import T_ProyectosForm, IntSocSettingsForm, FaseProyectoForm
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.contrib import messages
from .models import T_Proyectos, T_Gestion, T_Semestre, T_Materia, IntSocSettings
from django.contrib.auth.models import User

from django.views.generic import View


from django.core.mail import send_mail

from datetime import date

#permisos de grupo
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator   
from django.core.exceptions import PermissionDenied  



# vista de acceso publico
def hometrabajos(request):
    return render(request, 'homesocial/hometrabajos.html')

# Create your views here.
#formulario de agregacion docentes I.S.
#@user_passes_test(lambda u: permiso_Docentes(u, 'Docentes')) 
def proyecto_detail(request):
    settings = IntSocSettings.objects.first()
    hoy = date.today()
    habilitado = settings and (settings.fecha_inicio_habilitacion <= hoy <= settings.fecha_fin_habilitacion)
    tiempo_restante = settings.tiempo_restante() if settings else None

    if request.method == 'POST':
        form = T_ProyectosForm(request.POST, request.FILES)
        if habilitado and form.is_valid():
            proyecto = form.save(commit=False)  # No guardar todavía la instancia del modelo
            proyecto.S_persona = User.objects.get(user=request.user)  # Asignar la persona relacionada con el usuario autenticado
            proyecto.save()  # Ahora guardar la instancia del modelo
            return redirect('dashboard')  # Asegúrate de que 'dashboard' sea el nombre correcto de tu vista para el dashboard
    else:
        form = T_ProyectosForm()

    return render(request, 'homesocial/proyecto_detail.html', {
        'form': form,
        'habilitado': habilitado,
        'tiempo_restante': tiempo_restante,
    })

#clasificacion de enviados y no enviados
#@user_passes_test(lambda u: permiso_I_S(u, 'admISD')) 
def clasificar_proyectos(request):
    gestion_id = request.GET.get('gestion')
    materias = T_Materia.objects.all()
    gestiones = T_Gestion.objects.all()

    materias_con_proyectos = []
    materias_sin_proyectos = []

    for materia in materias:
        if gestion_id:
            proyectos = T_Proyectos.objects.filter(T_Materia=materia, T_Gestion_id=gestion_id)
        else:
            proyectos = T_Proyectos.objects.filter(T_Materia=materia)

        if proyectos.exists():
            materias_con_proyectos.append(materia)
        else:
            materias_sin_proyectos.append(materia)
    
    return render(request, 'homesocial/clasificar_proyectos.html', {
        'materias_con_proyectos': materias_con_proyectos,
        'materias_sin_proyectos': materias_sin_proyectos,
        'gestiones': gestiones,
        'selected_gestion': gestion_id
    })
    
    
#asignacion de fechas para subir trabajos
#@user_passes_test(lambda u: permiso_I_S(u, 'admISD')) 
def inv_soc_settings(request):
    settings = IntSocSettings.objects.first()
    if not settings:
        settings =  IntSocSettings()

    if request.method == 'POST':
        form = IntSocSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = IntSocSettingsForm(instance=settings)
    
    return render(request, 'homesocial/inv_soc_settings.html', {'form': form})

#vista del proyecto I.S. para docentes
@login_required
#@user_passes_test(lambda u: permiso_Docentes(u, 'Docentes')) 
def proyectosin_so(request):
    persona = request.user
    proyectos = T_Proyectos.objects.filter(S_persona=persona).order_by('-Id_Proyect')
    
    # Paginación para los proyectos, incluyendo el último proyecto
    paginator = Paginator(proyectos, 1)  # Muestra 1 proyecto por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'persona': persona,
        'page_obj': page_obj
    }
    return render(request, 'homesocial/proyectosin_so.html', context)

#poryectos interacion social vista general publica
def repoin(request):
    t_gestion_id = request.GET.get('T_Gestion')
    t_semestre_id = request.GET.get('T_Semestre')
    
    # Inicializar listaproyectos como vacío
    listaproyectos = T_Proyectos.objects.none()
    
    if t_gestion_id or t_semestre_id:
        listaproyectos = T_Proyectos.objects.all()
        
        if t_gestion_id:
            listaproyectos = listaproyectos.filter(T_Gestion_id=t_gestion_id)
        
        if t_semestre_id:
            listaproyectos = listaproyectos.filter(T_Materia__T_Semestre_id=t_semestre_id)
        
        listaproyectos = listaproyectos.order_by('Id_Proyect')  # Ordenar para garantizar el primer proyecto
    
    # Obtener el primer proyecto si existe, de lo contrario None
    primer_proyecto = listaproyectos.first() if listaproyectos.exists() else None
    
    context = {
        'primer_proyecto': primer_proyecto,
        't_gestiones': T_Gestion.objects.all(),
        't_semestres': T_Semestre.objects.all(),
        'listaproyectos': listaproyectos,
        'selected_t_gestion': t_gestion_id,
        'selected_t_semestre': t_semestre_id,
    }
    
    return render(request, 'homesocial/repoin.html', context)

######## TAREAS #########

from .models import T_Tipo_Proyecto, T_Gestion, T_Semestre, T_Materia
from .forms import TipoProyectoForm

def listart(request):
    tipos = T_Tipo_Proyecto.objects.all()
    return render(request, 'Tareas/Tipo/listart.html', {'tipos': tipos})

def creart(request):
    if request.method == "POST":
        form = TipoProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listart')
    else:
        form = TipoProyectoForm()
    return render(request, 'Tareas/Tipo/creart.html', {'form': form})

def editart(request, pk):
    tipo = get_object_or_404(T_Tipo_Proyecto, pk=pk)
    if request.method == "POST":
        form = TipoProyectoForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect('listart')
    else:
        form = TipoProyectoForm(instance=tipo)
    return render(request, 'Tareas/Tipo/editart.html', {'form': form})

def eliminart(request, pk):
    tipo = get_object_or_404(T_Tipo_Proyecto, pk=pk)
    if request.method == "POST":
        tipo.delete()
        return redirect('listart')
    return render(request, 'Tareas/Tipo/eliminart.html', {'object': tipo})