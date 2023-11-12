from django import forms
from .models import libro, comentario

class libroform(forms.ModelForm):
    class Meta:
        model = libro
        fields = '__all__'

class comentarioform(forms.ModelForm):
    class Meta:
        model = comentario
        fields = ['descripcion', 'calificacion']

  