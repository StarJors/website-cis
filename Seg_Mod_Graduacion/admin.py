from django.contrib import admin
from .models import  ProyectoFinal, Complementario, TutorExterno, Materia, Modalidad, Categoria, InveCientifica, ComentarioInvCientifica

class ProyectoFinalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'fecha', 'estado')
    search_fields = ('titulo', 'usuario__email')
    filter_horizontal = ('tribunales',)

admin.site.register(ProyectoFinal, ProyectoFinalAdmin)
admin.site.register(Complementario)
admin.site.register(TutorExterno)
admin.site.register(Materia)
admin.site.register(Modalidad)
admin.site.register(Categoria)
admin.site.register(InveCientifica)
admin.site.register(ComentarioInvCientifica)
