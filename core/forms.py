from django import forms
from .models import Licitacion, CustomUser, Preguntasbbdd
from django.contrib.auth.models import Group

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label="Correo")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")

class LicitacionForm(forms.ModelForm):
    class Meta:
        model = Licitacion
        fields = ['idLicitacion', 'nombreLicitacion', 'descripcionLicitacion', 'archivoLicitacion']
    
## SE AGREGA PARA CUANDO SE SUBA UN ARCHIVO NO SE SOBREESCRIBA EN LA BBDD
class SubirArchivoForm(forms.ModelForm):
    class Meta:
        model = Licitacion
        fields = ['archivoLicitacion']
    
    def __init__(self, *args, **kwargs):
        super(SubirArchivoForm, self).__init__(*args, **kwargs)
        # Campos de idLicitacion y nombreLicitacion solo lectura
        self.fields['idLicitacion'] = forms.CharField(initial=self.instance.idLicitacion, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
        self.fields['nombreLicitacion'] = forms.CharField(initial=self.instance.nombreLicitacion, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
        self.fields['descripcionLicitacion'] = forms.CharField(initial=self.instance.descripcionLicitacion, required=False, widget=forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'rows': 5}))

class PreguntasForm(forms.ModelForm):
    class Meta:
        model = Preguntasbbdd
        fields = ['idPreguntas', 'nombrePregunta']

# USUARIOS #
class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Contraseña')
    group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None, label='Rol')

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'first_name', 'last_name', 'rut', 'group']
        labels = {
            'email': 'Correo electrónico',
            'password': 'Contraseña',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'rut': 'RUT',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            user.groups.add(self.cleaned_data['group'])
        return user