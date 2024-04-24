from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

# Create your views here.

def home (request):
    return render(request, 'core/home.html')

def liccreac (request):
    return render(request, 'core/creacion_de_licitaciones.html')


# INGRESO DE SESION #def login_view(request):
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirige al home luego del login exitoso
            else:
                # Usuario no válido, mostrar mensaje de error
                mesg = "Usuario o contraseña incorrectos."
                return render(request, 'core/ingreso.html', {'form': form, 'mesg': mesg})
    else:
        form = LoginForm()
    return render(request, 'core/ingreso.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('home')