from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from Seg_Mod_Graduacion.models import ProyectoFinal, TutorExterno

User = get_user_model()

ESTADO_CHOICES = [
    ('Aprobado', 'Aprobado'),
    ('Pendiente', 'Pendiente'),
    ('Rechazado', 'Rechazado'),
]

# Filtrar usuarios que están en el grupo "Estudiantes" y cuyo estado es "Aprobado"
def estudiantes_aprobados():
    return User.objects.filter(groups__name='Estudiantes', estado=True)

# Modelo para Titulado, heredando datos de User y ProyectoFinal
class Titulado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Estudiantes', 'estado': True})
    proyecto_final = models.OneToOneField(ProyectoFinal, on_delete=models.CASCADE, limit_choices_to={'estado': 'Aprobado'})
    anio_ingreso = models.IntegerField()
    periodo_ingreso = models.CharField(max_length=50)
    anio_egreso = models.IntegerField()
    periodo_egreso = models.CharField(max_length=50)
    nota = models.FloatField()

    def __str__(self):
        return f"{self.usuario.nombre} {self.usuario.apellido} ({self.usuario.ru})"

# Modelo para Documento, relacionado con Titulado
class Documento(models.Model):
    titulado = models.ForeignKey(Titulado, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=250)
    modalidad = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    numero_acta = models.CharField(max_length=50)
    tribunales = models.ManyToManyField(User, related_name='tribunales_documento', limit_choices_to={'groups__name': 'Docentes'}, blank=True)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_documento', limit_choices_to={'groups__name': 'Docentes'})
    tutor_externo = models.ForeignKey(TutorExterno, on_delete=models.SET_NULL, null=True, blank=True)
    pdf_proyecto_final = models.FileField(upload_to='documentos/proyecto_final/')

    def __str__(self):
        return self.titulo