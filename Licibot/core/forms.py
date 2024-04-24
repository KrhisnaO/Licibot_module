from django import forms
from .models import Licitacion

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label="Correo")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    class Meta:
        fields = ['username', 'password']

class LicitacionForm(forms.ModelForm):
    idLicitacion = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 0, 'max': 100})),
    label="Idlicit"
    nombreLicitacion = forms.CharField(widget=forms.TextInput(), label="Nombre lic")
    class Meta:
        model = Licitacion
        fields = ['idLicitacion', 'nombreLicitacion']