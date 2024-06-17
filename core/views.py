from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Licitacion, Preguntasbbdd, Respuesta, ErrorHistory
from .forms import LoginForm, CreateUserForm, LicitacionForm, PreguntasForm, SubirArchivoForm, CustomPasswordResetForm
import requests
from django.db.models import Q
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .utils import obtener_licitaciones, subir_chatpdf, preguntar_chatpdf


# Create your views here.

def home(request):
    lici_count = Licitacion.objects.count()
    preg_count = Preguntasbbdd.objects.count()
    nolici_count = Licitacion.objects.filter(archivoLicitacion__isnull=True).count() + Licitacion.objects.filter(archivoLicitacion="").count()
    licidoc_count = Licitacion.objects.filter(~Q(archivoLicitacion__isnull=True) & ~Q(archivoLicitacion="")).count()
    return render(request, 'core/home.html', {'lici_count': lici_count, 'preg_count': preg_count, 'nolici_count':nolici_count, 'licidoc_count':licidoc_count})

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

## CAMBIAR CONTRASEÑA ###

def recuperar_pass(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']

            User = get_user_model()
            user = User.objects.get(email=email)

            user.set_password(new_password)
            user.save()
            return redirect('ingreso') 
    else:
        form = CustomPasswordResetForm()

    return render(request, 'core/recuperar_pass.html', {'form': form})


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
                user = form.save()
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

@login_required
def editar_usuario(request, user_id):
    usuario = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha actualizado la información exitosamente.')
            return redirect('historial_usu')
    else:
        form = CreateUserForm(instance=usuario)
    # Limpiar los mensajes después de recuperarlos
    storage = messages.get_messages(request)
    storage.used = False
    
    return render(request, 'core/editar_usuario.html', {'form': form})

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


#### MANTENEDOR DE PREGUNTAS #############################################
@login_required
def mantenedor_preguntas(request, action, id):
    data = {"mesg": "", "action": action, "id": id}

    try:
        if action == 'ins':
            if request.method == "POST":
                form = PreguntasForm(request.POST, request.FILES)
                if form.is_valid():
                    try:
                        form.save()
                        data["mesg"] = "¡La Pregunta fue creada correctamente!"
                    except Exception as e:
                        # Registrar el error en el historial
                        registrar_error(request, 'mantenedor_preguntas', f"Error al crear pregunta: {str(e)}")
                        data["mesg"] = "¡No se pudo crear la pregunta!"
            else:
                form = PreguntasForm()

        elif action == 'upd':
            objeto = Preguntasbbdd.objects.get(idPreguntas=id)
            if request.method == "POST":
                form = PreguntasForm(request.POST, request.FILES, instance=objeto)
                if form.is_valid():
                    try:
                        form.save()
                        data["mesg"] = "¡La Pregunta fue actualizada correctamente!"
                    except Exception as e:
                        # Registrar el error en el historial
                        registrar_error(request, 'mantenedor_preguntas', f"Error al actualizar pregunta: {str(e)}")
                        data["mesg"] = "¡No se pudo actualizar la pregunta!"
            else:
                form = PreguntasForm(instance=objeto)

        elif action == 'del':
            try:
                Preguntasbbdd.objects.get(idPreguntas=id).delete()
                data["mesg"] = "¡La Pregunta fue eliminada correctamente!"
                return redirect('mantenedor_preguntas', action='ins', id='-1')
            except Exception as e:
                # Registrar el error en el historial
                registrar_error(request, 'mantenedor_preguntas', f"Error al eliminar pregunta: {str(e)}")
                data["mesg"] = "¡No se pudo eliminar la pregunta!"

        data["list"] = Preguntasbbdd.objects.all().order_by('idPreguntas')
        data["form"] = form

    except Exception as e:
        # Registrar el error en el historial
        registrar_error(request, 'mantenedor_preguntas', f"Error en mantenedor de preguntas: {str(e)}")
        messages.error(request, 'Ha ocurrido un error al procesar la solicitud.')

    # Limpiar los mensajes después de recuperarlos
    storage = messages.get_messages(request)
    storage.used = False
    return render(request, "core/mantenedor_preguntas.html", data)


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

###################################################################
# SUBIR ARCHIVO DE LICITACIONES #
@login_required
def subir_archivo(request):
    licitacion_id = request.GET.get('id', None)
    licitacion = None
    id_encontrado = None
    error = None
    pregunta_id = 1  

    if licitacion_id:
        licitacion = get_object_or_404(Licitacion, idLicitacion=licitacion_id)

    if request.method == 'POST' and 'validar' in request.POST:
        form = SubirArchivoForm(request.POST, request.FILES, instance=licitacion if licitacion else None)
        if form.is_valid():
            archivo = form.cleaned_data.get('archivoLicitacion')
            if archivo:
                # Verificar que el archivo sea PDF
                if not archivo.name.endswith('.pdf'):
                    error = 'Solo se permiten archivos PDF.'
                else:
                    file_name = default_storage.save(archivo.name, ContentFile(archivo.read()))
                    file_path = default_storage.path(file_name)

                    source_id = subir_chatpdf(file_path)
                    if source_id:
                        pregunta = Preguntasbbdd.objects.get(idPreguntas=pregunta_id).nombrePregunta
                        respuesta_api = preguntar_chatpdf(source_id, pregunta, id_only=True)
                        if respuesta_api:
                            id_encontrado = respuesta_api.strip().split()[-1]  # Extraer solo el ID
                            if id_encontrado == str(licitacion.idLicitacion):
                                # Guardar la respuesta en la base de datos
                                pregunta_obj = Preguntasbbdd.objects.get(idPreguntas=pregunta_id)
                                Respuesta.objects.create(
                                    licitacion=licitacion,
                                    pregunta=pregunta_obj,
                                    textoRespuesta=id_encontrado
                                )
                                messages.success(request, 'Archivo validado correctamente. Ahora puede guardarlo.')
                                # Guardar el nombre del archivo en la sesión
                                request.session['file_name'] = file_name

                                # Redirigir a la seleccion preguntas
                                return redirect('seleccionar_preguntas', licitacion_id=licitacion.idLicitacion)
                            else:
                                error = 'El ID de la licitación en el archivo no coincide con el ID de la licitación seleccionada.'
                        else:
                            error = 'No se pudo obtener una respuesta de la API.'
                    else:
                        error = 'Error al subir el archivo PDF.'
            else:
                error = 'No se ha seleccionado ningún archivo para subir.'
        else:
            error = 'Error en el formulario.'

    if request.method == 'POST' and 'guardar' in request.POST:
        form = SubirArchivoForm(request.POST, instance=licitacion if licitacion else None)
        if form.is_valid():
            file_name = request.session.get('file_name')
            if file_name:
                file_path = default_storage.path(file_name)
                with open(file_path, 'rb') as f:
                    archivo = ContentFile(f.read(), name=file_name)
                if licitacion:
                    licitacion.archivoLicitacion = archivo
                    licitacion.save(update_fields=['archivoLicitacion'])
                    messages.success(request, '¡El archivo ha sido guardado con éxito!')
                    # Eliminar el nombre del archivo de la sesión
                    del request.session['file_name']
                    return redirect('subir_archivo')
                else:
                    messages.warning(request, 'No se ha seleccionado ninguna licitación.')
            else:
                messages.warning(request, 'No se ha seleccionado ningún archivo para subir o la validación no ha sido exitosa.')
        else:
            error = 'Error en el formulario.'
    else:
        form = SubirArchivoForm(instance=licitacion if licitacion else None)

    return render(request, 'core/subir_archivo.html', {'form': form, 'licitacion': licitacion, 'id_encontrado': id_encontrado, 'error': error})

# LEER ARCHIVOS PDF CON SUS RESPECTIVAS RESPUESTAS #
def leer_pdf(request, id):
    licitacion = get_object_or_404(Licitacion, idLicitacion=id)
    preguntas = Preguntasbbdd.objects.all()
    respuestas = Respuesta.objects.filter(licitacion=licitacion).select_related('pregunta')

    respuestas_dict = {respuesta.pregunta.idPreguntas: respuesta.textoRespuesta for respuesta in respuestas}

    preguntas_respuestas = []
    for pregunta in preguntas:
        preguntas_respuestas.append({
            'pregunta': pregunta,
            'respuesta': respuestas_dict.get(pregunta.idPreguntas, 'No hay respuesta')
        })

    return render(request, 'core/leer_pdf.html', {
        'licitacion': licitacion,
        'preguntas_respuestas': preguntas_respuestas,
    })


@login_required
def seleccionar_preguntas(request, licitacion_id):
    licitacion = get_object_or_404(Licitacion, idLicitacion=licitacion_id)
    preguntas = Preguntasbbdd.objects.all()

    if request.method == 'POST':
        preguntas_seleccionadas = request.POST.getlist('preguntas')
        if preguntas_seleccionadas:
            request.session['preguntas_seleccionadas'] = preguntas_seleccionadas
            return redirect('leer_pdf', id=licitacion_id)
        else:
            messages.error(request, 'Debe seleccionar al menos una pregunta.')

    return render(request, 'core/filtro_pregun.html', {'preguntas': preguntas, 'licitacion': licitacion})



### HISTORIAL DE ERRORES ##
@login_required
def registrar_error(request, tipo_vista, descripcion):
    error = ErrorHistory(
        tipo_vista=tipo_vista,
        descripcion=descripcion,
    )
    error.save()
    return redirect('home')

@login_required
def historial_errores(request):
    errores = ErrorHistory.objects.all().order_by('-fecha')
    return render(request, 'core/historial_errores.html', {'errores': errores})

### CONTEO LICITACIONES SIN ARCHIVO ###