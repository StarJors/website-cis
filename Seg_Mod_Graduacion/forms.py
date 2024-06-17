from django import forms
from Gestion_Usuarios import admin
from .models import InveCientifica, ComentarioInvCientifica



#class ProyectoFinalForm(forms.ModelForm):
#    class Meta:
#        model = ProyectoFinal
#        fields = '__all__'
#
#    def clean_tribunales(self):
#        tribunales = self.cleaned_data.get('tribunales')
#        if tribunales.count() != 3:
#            raise forms.ValidationError('Debe seleccionar exactamente 3 tribunales.')
#        return tribunales

#class ProyectoFinalAdmin(admin.ModelAdmin):
#    form = ProyectoFinalForm
#    list_display = ('titulo', 'usuario', 'fecha', 'estado')
#    search_fields = ('titulo', 'usuario__email')
#    filter_horizontal = ('tribunales',)

#admin.site.register(ProyectoFinal, ProyectoFinalAdmin)


class InveCientificaForm(forms.ModelForm):
    class Meta:
        model = InveCientifica
        fields = ['invtitulo', 'invdescripcion', 'invdocumentacion', 'invcategoria', 'invdestacado']
        widgets = {
            'invdescripcion': forms.Textarea(attrs={'class': 'descripcion-field'}),
        }
        
class InvComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioInvCientifica
        fields = ['invcomentario'] 
        widgets = {
            'invcomentario': forms.Textarea(attrs={'class': 'comentari-field'}),
        }       
        