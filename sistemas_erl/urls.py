from django.contrib import admin
from django.urls import path
from libro import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('iniciarsesion/', views.iniciarsesion, name='iniciarsesion'),
    path('Salir/', views.salir, name='Salir'),
    path('libros/', views.libros, name='libros'),
    path('crear_libro/', views.crear_libro, name='crear_libro'),
    path('editar_libro/<int:id>', views.editar_libro, name='editar_libro'),
    path('eliminar_libro/<int:id>', views.eliminar_libro, name='eliminar_libro'),
    path('comentarios/<int:id_libro>/', views.comentarios, name='comentarios'),
    path('agregar_comentario/<int:id_libro>/', views.agregar_comentario, name='agregar_comentario'),
    path('editarcomentarios/<int:id>', views.editar_comentario, name='editarcomentarios'),
    path('eliminar_comentario/<int:id>', views.eliminar_comentario, name='eliminar_comentario'),
    path('error_libro', views.error_libro, name='error_libro'),
    path('errorcomentario', views.errorcomentario, name='errorcomentario'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)