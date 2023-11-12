from typing import Any
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class libro(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100,verbose_name='Título', blank=False)
    imagen = models.ImageField(upload_to='imagenes/', verbose_name='Imagen', null=True)
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=False)

    def __str__(self):
        fila = "Título: " + self.titulo + " - " + "Descripción: " + self.descripcion
        return fila
    
    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()

class comentario(models.Model):
    titulo = models.CharField(max_length=150, blank=False)
    descripcion = models.TextField(blank=False)
    fecha = models.DateTimeField(auto_now_add=True)
    completado = models.DateTimeField(null=True)
    importante = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    libro = models.ForeignKey(libro, on_delete=models.CASCADE)
    calificacion = models.IntegerField(default=3)
    

    def __str__(self):
        return self.titulo + '- by ' + self.usuario.username