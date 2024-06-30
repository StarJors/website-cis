from django import forms
from .models import InvCientifica, ComentarioInvCientifica, InvSettings, PerfilProyecto, ComentarioPerfil,ProyectoFinal

# área de investigación científica 
class InvCientificaForm(forms.ModelForm):
    class Meta:
        model = InvCientifica
        fields = ['titulo', 'descripcion', 'documentacion', 'modalidad', 'destacado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'descripcion-field'}),
        }

class InvComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioInvCientifica
        fields = ['comentario'] 
        widgets = {
            'comentario': forms.Textarea(attrs={'class': 'comentari-field'}),
        }

class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = InvSettings
        fields = ['habilitarInv']

    def __init__(self, *args, **kwargs):
        super(GlobalSettingsForm, self).__init__(*args, **kwargs)
        
# área de perfil de proyecto 
class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilProyecto
        fields = ['titulo', 'descripcion', 'documentacion', 'modalidad']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'descripcion-field'}),
        }
        
class PerComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioPerfil
        fields = ['comentario'] 
        widgets = {
            'comentario': forms.Textarea(attrs={'class': 'comentari-field'}),
        }

class ProyectoFinalForm(forms.ModelForm):
    class Meta:
        model = ProyectoFinal
        fields = ['titulo', 'slug', 'resumen', 'modalidad', 'fecha', 'tribunales', 'tutor', 'tutor_externo', 'documentacion', 'estado']
