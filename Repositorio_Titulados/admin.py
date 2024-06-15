from django.contrib import admin
from Repositorio_Titulados.forms import DocumentoForm
from .models import Titulado, Documento, TutorExterno

class TituladoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'proyecto_final', 'anio_ingreso', 'periodo_ingreso', 'anio_egreso', 'periodo_egreso', 'nota')
    search_fields = ('usuario__nombre', 'usuario__apellido', 'usuario__ru')
    list_filter = ('anio_ingreso', 'anio_egreso')

class DocumentoAdmin(admin.ModelAdmin):
    form = DocumentoForm
    list_display = ('titulo', 'titulado', 'modalidad', 'fecha', 'numero_acta')
    search_fields = ('titulo', 'titulado__usuario__nombre', 'titulado__usuario__apellido')
    list_filter = ('modalidad', 'fecha')
    filter_horizontal = ('tribunales',)

admin.site.register(Titulado, TituladoAdmin)
admin.site.register(Documento, DocumentoAdmin)
