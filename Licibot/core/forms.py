from django import forms
from .models import Licitacion, CustomUser
from django.contrib.auth.models import Group

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label="Correo")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")

class LicitacionForm(forms.ModelForm):
    class Meta:
        model = Licitacion
        fields = ['idLicitacion', 'nombreLicitacion', 'archivoLicitacion']
        widgets = {
            'idLicitacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el ID de la licitación'
            }),
            'nombreLicitacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la licitación'
            }),
            'archivoLicitacion': forms.FileInput(attrs={
                'class': 'form-control-file'
            })
        }
        labels = {
            'idLicitacion': 'ID de la Licitación',
            'nombreLicitacion': 'Nombre de la Licitación',
            'archivoLicitacion': 'Subir Archivo (obligatorio)'
        }

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None, label='Rol')

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'rut', 'group']
        labels = {
            'username': 'Nombre de usuario',
            'password': 'Contraseña',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'rut': 'RUT',
        }

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        user.groups.add(self.cleaned_data['group'])
        if commit:
            user.save()
        return user