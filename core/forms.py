from django import forms
from .models import Licitacion, CustomUser, Preguntasbbdd
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

# USUARIOS #
class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Contraseña')
    group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None, label='Rol')
    is_active = forms.BooleanField(label='Activo', required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'rut', 'group', 'is_active']
        labels = {
            'email': 'Correo electrónico',
            'password': 'Contraseña',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'rut': 'RUT',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar los campos como requeridos solo en la creación, no en la edición
        if self.instance.pk:
            self.fields['password'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            user.groups.set([self.cleaned_data['group']])
        return user
    
### INGRESO ###

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label="Correo")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")

## CAMBIO DE CONTRASEÑA ##
class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    new_password = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("No hay ninguna cuenta asociada a este correo electrónico.")
        return email
    
########################################  
 
# VALIDAR ID DE LICITACION ##
class ValidarIDLicitacionForm(forms.Form):
    idLicitacion = forms.CharField(label='ID de Licitación', max_length=20)

class LicitacionForm(forms.ModelForm):
    class Meta:
        model = Licitacion
        fields = ['nombreLicitacion', 'descripcionLicitacion', 'archivoLicitacion', 'fechaCierre', 'estado', 'nombreOrganismo', 'diasCierreLicitacion']
    

## SE AGREGA PARA CUANDO SE SUBA UN ARCHIVO NO SE SOBREESCRIBA EN LA BBDD
class SubirArchivoForm(forms.ModelForm):
    class Meta:
        model = Licitacion
        fields = ['archivoLicitacion']

    def clean_archivoLicitacion(self):
        archivo = self.cleaned_data['archivoLicitacion']
        if archivo:
            extension = archivo.name.split('.')[-1].lower()
            if extension != 'pdf':
                raise forms.ValidationError('El archivo debe ser un PDF.')
        return archivo


### PREGUNTAS  ####

class PreguntasForm(forms.ModelForm):
    class Meta:
        model = Preguntasbbdd
        fields = ['idPreguntas', 'nombrePregunta']

