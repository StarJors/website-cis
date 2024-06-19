from django.shortcuts import render
from Gestion_Usuarios.models import models
from django.contrib.auth.models import Group

from django.shortcuts import render, redirect , HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from django.views import View
from .forms import InveCientificaForm, InvComentarioForm, GlobalSettingsForm, perfilForm, PerComentarioForm
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.contrib import messages
from Seg_Mod_Graduacion.models import InveCientifica, ComentarioInvCientifica, InvSettings, PerfildeProyecto, Comentarioperfil
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
def vista_investigacion(request):
    # Obtener todos los proyectos asociados al usuario en sesión
    proyectos_usuario = InveCientifica.objects.filter(user=request.user).order_by('-invfecha_creacion').prefetch_related('comentarioinvcientifica_set')

    # Paginación
    paginator = Paginator(proyectos_usuario, 1)  # Mostrar un proyecto por página
    page_number = request.GET.get('page')
    proyectos_paginados = paginator.get_page(page_number)

    return render(request, 'invcientifica/vista_investigacion.html', {'proyectos': proyectos_paginados})


#def agregar_comentario(request, proyecto_id):
#    proyecto = InveCientifica.objects.get(id=proyecto_id)
#    if request.method == 'POST':
#        formf = InvComentarioForm(request.POST)
#        if formf.is_valid():
#            invcomentario = formf.save(commit=False)
#           invcomentario.proyecto_relacionado = proyecto
#           invcomentario.user = request.user  # Asigna el usuario actual
#            invcomentario.save()
#            return redirect('dashboard', proyecto_id=proyecto_id)
#    else:
#        formf = InvComentarioForm()
#    return render(request, 'proyectos/agregar_comentario.html', {'formf': formf, 'proyecto': proyecto})

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
    
#aprovacion desabilitar proyecto 
#@user_passes_test(lambda u: permiso_I_S(u, 'admISD')) 

def global_settings_view(request):
    settings = InvSettings.objects.first()
    if not settings:
        settings = InvSettings()

    if request.method == 'POST':
        form = GlobalSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = GlobalSettingsForm(instance=settings)
    
    return render(request, 'invcientifica/global_settings.html', {'form': form, 'settings': settings})


@login_required
#@user_passes_test(lambda u: permiso_Estudiantes(u, 'Estudiantes')) 
def agregar_investigacion(request):
    settings = InvSettings.objects.first()
    
    if not settings:
        messages.error(request, 'No se encontró la configuración global. Por favor, contacta al administrador.')
        return redirect('global_settings')
    
 
    tiene_investigacion_aprobada = InveCientifica.objects.filter(user=request.user, investado='Aprobado').exists()
    
   
    form_disabled = not settings.habilitarInv or tiene_investigacion_aprobada
    
    if request.method == 'POST' and not form_disabled:
        form = InveCientificaForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
           
            slug = slugify(proyecto.invtitulo)
            counter = 1
            while InveCientifica.objects.filter(slug=slug).exists():
                slug = f"{slug}-{counter}"
                counter += 1
            proyecto.slug = slug
           
            proyecto.user = request.user
            proyecto.save()
            return redirect('dashboard')
    else:
        form = InveCientificaForm()
    
   
    if form_disabled:
        for field in form.fields.values():
            field.widget.attrs['disabled'] = 'disabled'
    
    return render(request, 'invcientifica/agregar_investigacion.html', {
        'form': form,
        'form_disabled': form_disabled,
    })
    
    
    
# perfil de proyecto 

@login_required
#@user_passes_test(lambda u: permiso_Estudiantes(u, 'Estudiantes')) 
def vista_perfil(request):
    proyectos_usuario = PerfildeProyecto.objects.filter(user=request.user).order_by('-perfecha_creacion').prefetch_related('comentarios')
    
    paginator = Paginator(proyectos_usuario, 1) 
    page_number = request.GET.get('page')
    proyectos_paginados = paginator.get_page(page_number)

    return render(request, 'perfil/vista_perfil.html', {'proyectos': proyectos_paginados})

#@method_decorator(user_passes_test(lambda u: permiso_M_G(u, 'admMG')), name='dispatch')
class PerfilesParaAprobar(View):
    def get(self, request):
        proyectos = PerfildeProyecto.objects.filter(perestado='Pendiente')
        proyectos_con_formulario = {proyecto: PerComentarioForm() for proyecto in proyectos}
        
        context = {
            'proyectos': proyectos_con_formulario,
        }
        return render(request, 'perfil/PerfilesParaAprobar.html', context)
    
    def post(self, request):
        proyecto_id = request.POST.get('proyecto_id')
        comentario_texto = request.POST.get('comentario_texto')
        if proyecto_id and comentario_texto:
            proyecto = get_object_or_404(PerfildeProyecto, pk=proyecto_id)
            Comentarioperfil.objects.create(percomentario=comentario_texto, user=request.user, perproyecto_relacionado=proyecto)
            messages.success(request, 'Comentario agregado exitosamente.')
        else:
            messages.error(request, 'Hubo un error al agregar el comentario.')
        
        if 'aprobar' in request.POST:
            return AprobarPerfil().post(request, proyecto_id)
        elif 'rechazar' in request.POST:
            return RechazarPerfil().post(request, proyecto_id)
        else:
            messages.error(request, 'Hubo un error al procesar la solicitud.')
            return redirect('PerfilesParaAprobar')
    
class AprobarPerfil(View):
    def post(self, request, proyecto_id):
        proyecto = get_object_or_404(PerfildeProyecto, pk=proyecto_id)
        proyecto.perestado = 'Aprobado'
        proyecto.save()
        messages.success(request, '¡Perfil aprobado exitosamente!')
        return redirect('PerfilesParaAprobar')

class RechazarPerfil(View):
    def post(self, request, proyecto_id):
        proyecto = get_object_or_404(PerfildeProyecto, pk=proyecto_id)
        proyecto.perestado = 'Rechazado'
        proyecto.save()
        messages.error(request, '¡Perfil rechazado!')
        return redirect('PerfilesParaAprobar')
    
#agregar nuevo perfil
def agregar_perfil(request):
    # Verificar si el usuario tiene al menos un InveCientifica con estado 'Aprobado'
    tiene_investigacion_aprobada = InveCientifica.objects.filter(user=request.user, investado='Aprobado').exists()
    
    # Deshabilitar el formulario si no tiene investigación aprobada
    form_disabled = not tiene_investigacion_aprobada

    if request.method == 'POST' and not form_disabled:
        form = perfilForm(request.POST, request.FILES)
        if form.is_valid():
            proyecto = form.save(commit=False)
        
            slug = slugify(proyecto.pertitulo)
            counter = 1
            while PerfildeProyecto.objects.filter(slug=slug).exists():
                slug = f"{slug}-{counter}"
                counter += 1
            proyecto.slug = slug
        
            proyecto.persona = request.user.persona
            proyecto.save()
            return redirect('dashboard')
    else:
        form = perfilForm()

    if form_disabled:
        for field in form.fields.values():
            field.widget.attrs['disabled'] = 'disabled'

    return render(request, 'perfil/agregar_perfil.html', {
        'form': form,
        'form_disabled': form_disabled,
    })