from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import libro, comentario
from .forms import libroform, comentarioform
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

def inicio(request):
    Libros = libro.objects.all()
    return render(request, 'inicio.html', {'libros': Libros})


def registro(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {
            'form': UserCreationForm()
        })
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                try:
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1']
                    )
                    user.save()
                    login(request, user)
                    return redirect('inicio')
                except IntegrityError:
                    return render(request, 'registro.html', {
                        'form': form,
                        'error': 'El usuario ya existe'
                    })
            else:
                return render(request, 'registro.html', {
                    'form': form,
                    'error': 'Las contraseñas no coinciden'
                })
        else:
            return render(request, 'registro.html', {
                'form': form,
                'error': 'Por favor, complete el formulario correctamente'
            })

def iniciarsesion(request):
    ##
    if request.user.is_authenticated:
        return redirect('inicio')
    ##

    if request.method == 'GET':
        return render(request, 'iniciarsesion.html', {
            'form': AuthenticationForm
        })
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'iniciarsesion.html', {
                'form': AuthenticationForm,
                'error': 'El Usuario o la Contrasena son incorrectos'
            })
        else:
            if user.is_superuser:
                login(request, user)  
                return redirect('libros')
            ##El cambio esta aqui, si el usuario tiene el superuser
            ###puede ir a libros si no que coma mierda el usuario XD
            else:
                login(request, user)
                return redirect('inicio')
            
def salir(request):
    logout(request)
    return redirect('inicio')

@user_passes_test(lambda u: u.is_superuser, login_url='error_libro')
##El user_passes_test indica que solo un super usuario puede entrar a esta pagina
##el que no sea super usuario lo manda a la pagina error
def libros(request):
    libros = libro.objects.all()
    return render(request, 'libros.html', {'libros': libros})

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='error_libro')
##El user_passes_test indica que solo un super usuario puede entrar a esta pagina
##el que no sea super usuario lo manda a la pagina error
def crear_libro(request):
    if request.method == 'POST':
        formulario = libroform(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, '¡El libro se ha guardado correctamente!')
            return redirect('libros')
        else:
            messages.error(request, 'Faltan campos obligatorios. Por favor, completa todos los campos.')
    else:
        formulario = libroform()
    
    return render(request, 'crear_libro.html', {'formulario': formulario})
@user_passes_test(lambda u: u.is_superuser, login_url='error_libro')
def editar_libro(request, id):
    Libro = libro.objects.get(id=id)
    if request.method == 'POST':
        formulario = libroform(request.POST, request.FILES, instance=Libro)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, '¡El libro se ha guardado correctamente!')
            return redirect('libros')
        else:
            messages.error(request, 'Faltan campos obligatorios. Por favor, completa todos los campos.')
    else:
        formulario = libroform(instance=Libro)
    return render(request, 'editar_libro.html', {'formulario': formulario})

@user_passes_test(lambda u: u.is_superuser, login_url='error_libro')
def eliminar_libro(request, id):
    libro_obj = get_object_or_404(libro, id=id)
    url_libros = reverse('libros') 
    if request.method == 'POST':
        # Si se confirma la eliminación del libro
        libro_obj.delete()
        messages.success(request, 'El libro ha sido eliminado exitosamente.')
        return redirect(url_libros)
    return render(request, 'eliminar_libro.html', {'libro': libro_obj})

def comentarios(request, id_libro):
    libro_obj = libro.objects.get(id=id_libro)
    comentarios = comentario.objects.filter(libro=libro_obj)
    return render(request, 'comentarios.html', {'comentarios': comentarios, 'libro': libro_obj})

@login_required(login_url='/iniciarsesion/')
def agregar_comentario(request, id_libro):
    libros = libro.objects.all()  # obtén todos los libros
    if request.method == 'POST':
        calificacion = request.POST.get('calificacion')
        form = comentarioform(request.POST)
        if form.is_valid():
            new_comentario = form.save(commit=False)
            new_comentario.usuario = request.user
            libro_obj = libro.objects.get(id=id_libro)
            new_comentario.libro = libro_obj
            if calificacion:
                new_comentario.calificacion = int(calificacion)
            else:
                return render(request, 'agregar_comentario.html', {
                    'formulario': form,
                    'libros': libros,
                })
            new_comentario.save()
            id_libro = new_comentario.libro.id
            messages.success(request, '¡El comentario se ha guardado correctamente!')
            url_comentarios = reverse('comentarios', kwargs={'id_libro': id_libro})
            return redirect(url_comentarios)
        else:
            print(form.errors)
            return render(request, 'agregar_comentario.html', {
                'formulario': form,
                'libros': libros,
                'error': 'Por favor, complete el formulario correctamente'
            })
    else:
        form = comentarioform()
        return render(request, 'agregar_comentario.html', {'formulario': form, 'libros': libros})

def editar_comentario(request, id):
    comentario_editar = comentario.objects.get(id=id)
    if request.user != comentario_editar.usuario:
        return redirect('errorcomentario')
    
    libros = libro.objects.all()
    
    if request.method == 'POST':
        formulario = comentarioform(request.POST, request.FILES, instance=comentario_editar)
        if formulario.is_valid():
            comentario_editado = formulario.save(commit=False)
            comentario_editado.calificacion = request.POST.get('calificacion', 0)
            comentario_editado.save()
            messages.success(request, '¡El comentario se ha editado correctamente!')
            return redirect('comentarios', id_libro=comentario_editado.libro.id)
        else:
            messages.error(request, 'Complete todos los campos por favor')
    else:
        formulario = comentarioform(instance=comentario_editar)
    
    return render(request, 'editar_comentario.html', {'formulario': formulario, 'libros': libros})
def eliminar_comentario(request, id):
    comentario_obj = get_object_or_404(comentario, id=id)
    url_comentario = reverse('comentarios', args=[comentario_obj.libro.id]) 
    
    if comentario_obj.usuario != request.user:
        return redirect('errorcomentario')

    if request.method == 'POST':
        # Si se confirma la eliminación del comentario
        comentario_obj.delete()
        messages.success(request, 'El comentario ha sido eliminado exitosamente.')
        return redirect(url_comentario)

    return render(request, 'eliminar_comentario.html', {'comentario': comentario_obj})

def error_libro(request):
    return render(request, 'error_libro.html')

def errorcomentario(request):
    return render(request, 'errorcomentario.html')