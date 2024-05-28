from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Licitacion, Preguntasbbdd
from .forms import LoginForm, CreateUserForm, LicitacionForm, PreguntasForm, SubirArchivoForm
import requests

from .utils import obtener_licitaciones

# Create your views here.

def home(request):
    lici_count = Licitacion.objects.count()
    preg_count = Preguntasbbdd.objects.count()
    return render(request, 'core/home.html', {'lici_count': lici_count, 'preg_count': preg_count})

#### MANTENEDOR DE PREGUNTAS #############################################
@login_required
def mantenedor_preguntas(request, action, id):
    data = {"mesg": "", "action": action, "id": id}

    if action == 'ins':
        if request.method == "POST":
            form = PreguntasForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    form.save()
                    data["mesg"] = "¡La Pregunta fue creada correctamente!"
                except:
                    data["mesg"] = "¡No se puede crear dos Preguntas con la misma id!"
        else:
            form = PreguntasForm()

    elif action == 'upd':
        objeto = Preguntasbbdd.objects.get(idPreguntas=id)
        if request.method == "POST":
            form = PreguntasForm(request.POST, request.FILES, instance=objeto)
            if form.is_valid():
                form.save()
                data["mesg"] = "¡La Pregunta fue actualizada correctamente!"
        else:
            form = PreguntasForm(instance=objeto)

    elif action == 'del':
        try:
            Preguntasbbdd.objects.get(idPreguntas=id).delete()
            data["mesg"] = "¡La Pregunta fue eliminada correctamente!"
            return redirect('mantenedor_preguntas', action='ins', id='-1')
        except:
            data["mesg"] = "¡La Pregunta ya estaba eliminada!"
    data["list"] = Preguntasbbdd.objects.all().order_by('idPreguntas')
    data["form"] = form

    # Limpiar los mensajes después de recuperarlos
    storage = messages.get_messages(request)
    storage.used = False

    return render(request, "core/mantenedor_preguntas.html", data)

##### INGRESO DE SESION ###################################################
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

    # Limpiar los mensajes después de recuperarlos
    storage = messages.get_messages(request)
    storage.used = False

    return render(request, 'core/crear_usuario.html', {'form': form})


# HISTORIAL DE USUARIO #
@login_required
def historial_usu(request):
    usuarios = CustomUser.objects.all()  

    # Limpiar los mensajes después de recuperarlos
    storage = messages.get_messages(request)
    storage.used = False

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

# BUSCAR LICITACIONES #
@login_required
def buscar_lici(request):
    filtro_id = request.GET.get('id', None)
    filtro_palabra_clave = request.GET.get('palabra_clave', None)
    
    licitaciones = None
    if filtro_id or filtro_palabra_clave:
        licitaciones = obtener_licitaciones(filtro_id=filtro_id, filtro_palabra_clave=filtro_palabra_clave)
    
    if licitaciones is not None:
        if request.method == 'POST':
            # Procesar el formulario de guardado
            id_licitacion = request.POST.get('id_licitacion')
            nombre_licitacion = request.POST.get('nombre_licitacion')
            descripcion_licitacion = request.POST.get('descripcion_licitacion')
            
            # Verificar si la licitación ya existe en la base de datos
            if not Licitacion.objects.filter(idLicitacion=id_licitacion).exists():
                Licitacion.objects.create(
                    idLicitacion=id_licitacion,
                    nombreLicitacion=nombre_licitacion,
                    descripcionLicitacion=descripcion_licitacion
                )
                messages.success(request, '¡La licitación ha sido guardada con éxito!')
            else:
                messages.warning(request, 'La licitación ya existe en la base de datos.')
            return redirect('buscar_lici')
        
        return render(request, 'core/buscar_lici.html', {'licitaciones': licitaciones})
    elif filtro_id or filtro_palabra_clave:
        return render(request, 'core/buscar_lici.html', {'error_message': 'No se encontraron licitaciones con los criterios proporcionados.'})
    else:
        return render(request, 'core/buscar_lici.html')

# HISTORIAL LICITACIONES #
@login_required
def historial_lici(request):
    licitaciones_guardadas = Licitacion.objects.all()
    return render(request, 'core/historial_lici.html', {'licitaciones_guardadas': licitaciones_guardadas})

# SUBIR ARCHIVO DE LICITACIONES #
@login_required
def subir_archivo(request):
    licitacion_id = request.GET.get('id', None)
    licitacion = None

    if licitacion_id:
        licitacion = get_object_or_404(Licitacion, idLicitacion=licitacion_id)

    if request.method == 'POST':
        form = SubirArchivoForm(request.POST, request.FILES, instance=licitacion if licitacion else None)
        if form.is_valid():
            archivo = form.cleaned_data.get('archivoLicitacion')
            if archivo:
                if licitacion:
                    licitacion.archivoLicitacion = archivo
                    licitacion.save(update_fields=['archivoLicitacion'])
                    messages.success(request, '¡El archivo ha sido subido con éxito!')
                    return redirect('subir_archivo')
                else:
                    messages.warning(request, 'No se ha seleccionado ninguna licitación.')
            else:
                messages.warning(request, 'No se ha seleccionado ningún archivo para subir.')
    else:
        form = SubirArchivoForm(instance=licitacion)

    return render(request, 'core/subir_archivo.html', {'form': form, 'licitacion': licitacion})

