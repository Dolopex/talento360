from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    class Meta:
        model = Usuario  
        fields = ['username', 'password']
    

class RegistroUsuarioForm(forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'username', 'imagen', 'email', 'celular', 'genero', 'cargo','usuario_administrador']

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Identificacion o Clave invalidos, por favor intente nuevamente.",
        'inactive': "Esta cuenta está inactiva.",
    }
        
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombres', 'apellidos', 'email', 'celular', 'genero', 'direccion', 'imagen', 'pais', 'fecha_nacimiento']
        
class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'