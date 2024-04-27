
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser 
from .forms import LoginForm, CreateUserForm, LicitacionForm
import requests
# Create your views here.

def home (request):
    return render(request, 'core/home.html')

@login_required
def liccreac (request):
    return render(request, 'core/creacion_de_licitaciones.html')

def create_licitacion(request):
    if request.method == 'POST':
        form = LicitacionForm(request.POST, request.FILES)
        if form.is_valid():
            # Extraemos los datos necesarios para la verificación
            id_licitacion = form.cleaned_data['idLicitacion']
            nombre_licitacion = form.cleaned_data['nombreLicitacion']

            # Verificamos si existe alguna licitación con el mismo ID o nombre
            if create_licitacion.objects.filter(idLicitacion=id_licitacion).exists():
                messages.error(request, f'Una licitación con el ID {id_licitacion} ya existe.')
                return render(request, 'core/creacion_de_licitaciones.html', {'form': form})

            if create_licitacion.objects.filter(nombreLicitacion=nombre_licitacion).exists():
                messages.error(request, f'Una licitación con el nombre "{nombre_licitacion}" ya existe.')
                return render(request, 'core/creacion_de_licitaciones.html', {'form': form})

            # Si no existe, guardamos la nueva licitación
            form.save()
            messages.success(request, 'Licitación creada exitosamente.')
            return redirect('crear_licitaciones.html')  # Asegúrate de usar el nombre correcto de la URL

    else:
        form = LicitacionForm()

    return render(request, 'core/creacion_de_licitaciones.html', {'form': form})

# INGRESO DE SESION :
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                if user.is_superuser:
                    return redirect('crear_usuario')
                elif user.groups.filter(name='VENDEDOR').exists():
                    return redirect('vendedor')
                elif user.groups.filter(name='GERENTE').exists():
                    return redirect('gerente')
                else:
                    return redirect('home')
            else:
                mesg = "Usuario o contraseña incorrectos."
                return render(request, 'core/ingreso.html', {'form': form, 'mesg': mesg})
    else:
        form = LoginForm()
    return render(request, 'core/ingreso.html', {'form': form})

# CREADOR DE USUARIOS #
@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            if CustomUser.objects.filter(rut=rut).exists():
                messages.error(request, 'Ya existe un usuario con este RUT.')
            else:
                group = form.cleaned_data['group']

                user = CustomUser(
                    rut=rut,
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                )
                user.set_password(rut)
                user.save()
                user.groups.add(group)

                messages.success(request, 'El usuario se ha creado correctamente.')

                return redirect('crear_usuario')  
    else:
        form = CreateUserForm()

    return render(request, 'core/crear_usuario.html', {'form': form})


# HISTORIAL DE USUARIO #
@login_required
def historial_usu(request):
    usuarios = CustomUser.objects.all()  
    return render(request, 'core/historial_usu.html', {'usuarios': usuarios})

# CERRAR SESION ##
@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

# LOGIN ADMINISTRADR #
@login_required
def administrador(request):
    return render(request, 'core/administrador.html')

# LOGIN VENDEDOR #
@login_required
def vendedor(request):
    return render(request, 'core/vendedor.html')

# LOGIN GERENTE #
@login_required
def gerente(request):
    return render(request, 'core/gerente.html')

# PREGUNTAS #


# SUBIR ARCHIVO PDF #


###################################################################
# SUBIR ARCHIVO PDF #

