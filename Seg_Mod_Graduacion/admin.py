from django.contrib import admin
from .models import InvCientifica, Perfil, ProyectoFinal, Complementario, TutorExterno, Materia, Modalidad

class ProyectoFinalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'fecha', 'estado')
    search_fields = ('titulo', 'usuario__email')
    filter_horizontal = ('tribunales',)

admin.site.register(InvCientifica)
admin.site.register(Perfil)
admin.site.register(ProyectoFinal, ProyectoFinalAdmin)
admin.site.register(Complementario)
admin.site.register(TutorExterno)
admin.site.register(Materia)
admin.site.register(Modalidad)
