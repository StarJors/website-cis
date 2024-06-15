from django import forms
from .models import Documento

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        titulado = cleaned_data.get('titulado')
        if not titulado or titulado.usuario.estado != 'Aprobado':
            raise forms.ValidationError('El titulado seleccionado no está aprobado.')
        return cleaned_data
