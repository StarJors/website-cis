from django.shortcuts import render
from Gestion_Usuarios.models import models
from django.contrib.auth.models import Group

from django.shortcuts import render, redirect , HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.views import View
from .forms import InveCientificaForm, InvComentarioForm
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.contrib import messages
from Seg_Mod_Graduacion.models import InveCientifica, ComentarioInvCientifica
from django.contrib.auth.models import User

from django.views.generic import View


from django.core.mail import send_mail

from datetime import date

#permisos de grupo
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator   
from django.core.exceptions import PermissionDenied  
# Create your views here.

##############  permisos decoradores  para funciones y clases   ################  

#modalidad de gradiacion permigroup 
def permiso_M_G(user, ADMMGS):
    try:
        grupo = Group.objects.get(name=ADMMGS)
    except Group.DoesNotExist:
        raise PermissionDenied(f"El grupo '{ADMMGS}' no existe.")
    
    if grupo in user.groups.all():
        return True
    else:
        raise PermissionDenied

#docentes interaccion social permigroup
def permiso_I_S(user, ADMIIISP):
    try:
        grupo = Group.objects.get(name=ADMIIISP)
    except Group.DoesNotExist:
        raise PermissionDenied(f"El grupo '{ADMIIISP}' no existe.")
    
    if grupo in user.groups.all():
        return True
    else:
        raise PermissionDenied

#permiso para docentes  
def permiso_Docentes(user, Docentes):
    try:
        grupo = Group.objects.get(name=Docentes)
    except Group.DoesNotExist:
        raise PermissionDenied(f"El grupo '{Docentes}' no existe.")
    
    if grupo in user.groups.all():
        return True
    else:
        raise PermissionDenied

#permiso para estudiantes
def permiso_Estudiantes(user, Estudiantes):
    try:
        grupo = Group.objects.get(name=Estudiantes)
    except Group.DoesNotExist:
        raise PermissionDenied(f"El grupo '{Estudiantes}' no existe.")
    
    if grupo in user.groups.all():
        return True
    else:
        raise PermissionDenied

#vista 403
def handle_permission_denied(request, exception):
    return render(request, '403.html', status=403)

###############  general vistas   ####################################

def prueba(request):
    grupos = Group.objects.all()
    return render(request, "prueba.html", {'grupos': grupos})

################  vistas modalidad de graduacion  ##########################

#vista agregar formulario alcanze de proyecto 
@login_required
#@user_passes_test(lambda u: permiso_Estudiantes(u, 'Estudiantes')) 
def agregar_investigacion(request):
    if request.method == 'POST':
        form = InveCientificaForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
            # Generar un slug único para el proyecto
            slug = slugify(proyecto.invtitulo)
            counter = 1
            while InveCientifica.objects.filter(slug=slug).exists():
                slug = f"{slug}-{counter}"
                counter += 1
            proyecto.slug = slug
            # Asignar el usuario asociado al usuario actual
            proyecto.user = request.user
            proyecto.save()
            return redirect('dashboard')
    else:
        form = InveCientificaForm()
    return render(request, 'invcientifica/agregar_investigacion.html', {'form': form})

@login_required
#@user_passes_test(lambda u: permiso_Estudiantes(u, 'Estudiantes')) 
def vista_investigacion(request):
    # Obtener todos los proyectos asociados al usuario en sesión
    proyectos_usuario = InveCientifica.objects.filter(user=request.user).order_by('-invfecha_creacion').prefetch_related('comentarioinvcientifica_set')

    # Paginación
    paginator = Paginator(proyectos_usuario, 1)  # Mostrar un proyecto por página
    page_number = request.GET.get('page')
    proyectos_paginados = paginator.get_page(page_number)

    return render(request, 'invcientifica/vista_investigacion.html', {'proyectos': proyectos_paginados})


def agregar_comentario(request, proyecto_id):
    proyecto = InveCientifica.objects.get(id=proyecto_id)
    if request.method == 'POST':
        formf = InvComentarioForm(request.POST)
        if formf.is_valid():
            invcomentario = formf.save(commit=False)
            invcomentario.proyecto_relacionado = proyecto
            invcomentario.user = request.user  # Asigna el usuario actual
            invcomentario.save()
            return redirect('dashboard', proyecto_id=proyecto_id)
    else:
        formf = InvComentarioForm()
    return render(request, 'proyectos/agregar_comentario.html', {'formf': formf, 'proyecto': proyecto})

#@method_decorator(user_passes_test(lambda u: permiso_M_G(u, 'admMG')), name='dispatch')
class ProyectosParaAprobar(View):
    def get(self, request):
        proyectos = InveCientifica.objects.filter(investado='Pendiente')
        proyectos_con_formulario = {proyecto: InvComentarioForm() for proyecto in proyectos}
        
        context = {
            'proyectos': proyectos_con_formulario,
        }
        return render(request, 'invcientifica/ProyectosParaAprobar.html', context)
    
    def post(self, request):
        proyecto_id = request.POST.get('proyecto_id')
        comentario_texto = request.POST.get('comentario_texto')
        if proyecto_id and comentario_texto:
            proyecto = get_object_or_404(InveCientifica, pk=proyecto_id)
            ComentarioInvCientifica.objects.create(invcomentario=comentario_texto, user=request.user, invproyecto_relacionado=proyecto)
            messages.success(request, 'Comentario agregado exitosamente.')
        else:
            messages.error(request, 'Hubo un error al agregar el comentario.')
        
        if 'aprobar' in request.POST:
            return AprobarProyecto().post(request, proyecto_id)
        elif 'rechazar' in request.POST:
            return RechazarProyecto().post(request, proyecto_id)
        else:
            messages.error(request, 'Hubo un error al procesar la solicitud.')
            return redirect('ProyectosParaAprobar')

class AprobarProyecto(View):
    def post(self, request, proyecto_id):
        proyecto = get_object_or_404(InveCientifica, pk=proyecto_id)
        proyecto.investado = 'Aprobado'
        proyecto.save()
        messages.success(request, '¡Proyecto aprobado exitosamente!')
        return redirect('ProyectosParaAprobar')

class RechazarProyecto(View):
    def post(self, request, proyecto_id):
        proyecto = get_object_or_404(InveCientifica, pk=proyecto_id)
        proyecto.investado = 'Rechazado'
        proyecto.save()
        messages.error(request, '¡Proyecto rechazado!')
        return redirect('ProyectosParaAprobar')
#aprovacion de alcanze de proyecto 

