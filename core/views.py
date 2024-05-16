from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Licitacion, Preguntasbbdd
from .forms import LoginForm, CreateUserForm, LicitacionForm, PreguntasForm
import requests

# Create your views here.

## SE UTILIZA HOME PARA QUE LA API CORRA UNA VEZ INICIADA LA PAGINA WEB ##

def home(request):
    # CONSULTA POR LICITACIONES ACTIVAS
    url_api = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json?estado=activas&ticket=F8537A18-6766-4DEF-9E59-426B4FEE2844"

    # Envía una solicitud GET a la URL de la API
    respuesta = requests.get(url_api)

    # Verifica si la solicitud fue exitosa
    if respuesta.status_code == 200:
        # Convierte la respuesta en un objeto JSON
        datos = respuesta.json()
        listado = datos.get('Listado', [])

        # Filtra las licitaciones que contienen 'oFicinA' en el nombre
        licitaciones_filtradas = [licitacion for licitacion in listado if 'oFicinA'.upper() in licitacion.get('Nombre', '').upper()]

        # Renderiza el template con el listado de licitaciones filtradas como contexto
        return render(request, 'core/home.html', {'licitaciones': licitaciones_filtradas})
    else:
        # Si la solicitud no fue exitosa, devuelve un mensaje de error
        return render(request, 'core/home.html', {'error_message': 'No se pudieron obtener las licitaciones'})


#### SUBIR ARCHIVO PDF #########################################################
@login_required
def create_licitacion(request, action, id):
    data = {"mesg": "", "form": LicitacionForm, "action": action, "id": id}

    if action == 'ins':
        if request.method == "POST":
            form = LicitacionForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                    data["mesg"] = "¡La Licitacion fue creada correctamente!"
                except:
                    data["mesg"] = "¡No se puede crear dos licitaciones con la misma id!"

    elif action == 'upd':
        objeto = Licitacion.objects.get(idLicitacion=id)
        if request.method == "POST":
            form = LicitacionForm(data=request.POST, files=request.FILES, instance=objeto)
            if form.is_valid:
                form.save()
                data["mesg"] = "¡La Licitacion fue actualizada correctamente!"
        data["form"] = LicitacionForm(instance=objeto)

    elif action == 'del':
        try:
            Licitacion.objects.get(idLicitacion=id).delete()
            data["mesg"] = "¡La Licitacion fue eliminada correctamente!"
            return redirect(Licitacion, action='ins', id = '-1')
        except:
            data["mesg"] = "¡La Licitacion ya estaba eliminada!"

    data["list"] = Licitacion.objects.all().order_by('idLicitacion')
    return render(request, "core/creacion_de_licitaciones.html", data)

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



