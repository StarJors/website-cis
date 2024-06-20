from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from datetime import date
from django.conf import settings

User = get_user_model()

ESTADO_CHOICES = [
    ('Aprobado', 'Aprobado'),
    ('Pendiente', 'Pendiente'),
    ('Rechazado', 'Rechazado'),
]

class TutorExterno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Materia(models.Model):
    sigla = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    plan = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.sigla})"

class Modalidad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre}"
    
    
################      Primera fase Modalidad de Graduacion       ####################

class Categoria(models.Model):
    nombrecategoria = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nombrecategoria
    
    
class InveCientifica(models.Model):
    invtitulo = models.CharField(max_length=150, verbose_name='Agregar Titulo')
    slug = models.SlugField(unique=True)
    invfecha_creacion = models.DateTimeField(auto_now_add=True)
    invdescripcion = models.TextField(verbose_name='Agregar una Descripcion', blank=True)
    invdocumentacion = models.FileField(upload_to='documento/proyecto', verbose_name='Agregar Documentacion', null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario relacionado')
    invcategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Seleccione Una Modalidad')
    invdestacado = models.BooleanField(default=True, verbose_name='Destacar Formulario') 
    investado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')
    
    def __str__(self):
        return self.invtitulo
        
#agregar comentario formulario proyecto 
class ComentarioInvCientifica(models.Model):
    invcomentario = models.TextField(max_length=1000, help_text='',verbose_name='Ingrese Comentario Retroalimentativo')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    invFecha_post = models.DateTimeField(auto_now_add=True)
    invproyecto_relacionado = models.ForeignKey(InveCientifica, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-invFecha_post']

    def __str__(self):
        len_title = 15
        if len(self.invcomentario) > len_title:
            return self.invcomentario[:len_title] + '...'
        return self.invcomentario
    
    
class InvSettings(models.Model):
    habilitarInv = models.BooleanField(default=True, verbose_name='Habilitar Formulario')

    def __str__(self):
        return "Configuración Global"
    
##############################     Agregacion 2da Parte Perfil de poryecto   ##############

class PerfildeProyecto(models.Model):
    pertitulo = models.CharField(max_length=150, verbose_name='Agregar Titulo')
    slug = models.SlugField(unique=True)
    perfecha_creacion = models.DateTimeField(auto_now_add=True)
    perdescripcion = models.TextField(verbose_name='Agregar una Descripcion', blank=True)
    perdocumentacion = models.FileField(upload_to='documento/proyecto', verbose_name='Agregar Documentacion', null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuario relacionado')
    percategoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Seleccione Una Modalidad')
    perestado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')
    
    def __str__(self):
        return self.pertitulo
        
#agregar comentario formulario proyecto 
class Comentarioperfil(models.Model):
    percomentario = models.TextField(max_length=1000, help_text='',verbose_name='Ingrese Comentario Retroalimentativo')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    perFecha_post = models.DateTimeField(auto_now_add=True)
    perproyecto_relacionado = models.ForeignKey(PerfildeProyecto, on_delete=models.CASCADE, related_name='comentarios')
    
    class Meta:
        ordering = ['-perFecha_post']
    def __str__(self):
        return self.percomentario[:15] + '...' if len(self.percomentario) > 15 else self.percomentario
##############################     Agregacion 3da Parte  poryecto  final ##############

class InvCientifica(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=250)
    resumen = models.TextField(max_length=500)
    fecha = models.DateField(default=timezone.now)
    pdf_inv_c = models.FileField(upload_to='documentos/investigacion/')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return self.titulo
    

class Perfil(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=250)
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    pdf_perfil = models.FileField(upload_to='documentos/perfil/')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return self.titulo

class ProyectoFinal(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=250)
    resumen = models.TextField(max_length=500)
    modalidad = models.ForeignKey(Modalidad, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    tribunales = models.ManyToManyField(User, related_name='tribunales', limit_choices_to={'groups__name': 'Docentes'}, blank=True)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_final', limit_choices_to={'groups__name': 'Docentes'})
    tutor_externo = models.ForeignKey(TutorExterno, on_delete=models.SET_NULL, null=True, blank=True)
    pdf_proyecto_final = models.FileField(upload_to='documentos/proyecto_final/')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return self.titulo
