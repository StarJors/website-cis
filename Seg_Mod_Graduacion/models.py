from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

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

class Complementario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    anio_egreso = models.IntegerField()
    periodo_egreso = models.CharField(max_length=50)
    numero_acta = models.CharField(max_length=50)
    nota = models.FloatField()

    def __str__(self):
        return f"{self.usuario} - {self.anio_egreso}"
