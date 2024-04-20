from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label="Correo")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    class Meta:
        fields = ['username', 'password']
