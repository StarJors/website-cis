from django import forms
from Gestion_Usuarios import admin
from .models import InveCientifica, ComentarioInvCientifica, InvSettings, PerfildeProyecto, Comentarioperfil



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

# area de investigacion cientifica 
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


        
class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = InvSettings
        fields = ['habilitarInv']

    def __init__(self, *args, **kwargs):
        super(GlobalSettingsForm, self).__init__(*args, **kwargs)
        
#area de perfil de proyecto 
class perfilForm(forms.ModelForm):
    class Meta:
        model = PerfildeProyecto
        fields = ['pertitulo', 'perdescripcion', 'perdocumentacion', 'percategoria']
        widgets = {
            'perdescripcion': forms.Textarea(attrs={'class': 'descripcion-field'}),
        }
        
class PerComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentarioperfil
        fields = ['percomentario'] 
        widgets = {
            'percomentario': forms.Textarea(attrs={'class': 'comentari-field'}),
        }       

