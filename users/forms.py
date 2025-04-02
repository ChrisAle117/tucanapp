from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        strip=False,
        help_text='Ingrese una contraseña válida.',
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}),
        strip=False,
        help_text='Ingrese la misma contraseña nuevamente.',
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nombre', 'apellidos', 'rol', 'detalles']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Apellidos'}),
            'rol': forms.Select(attrs={'placeholder': 'Rol'}),
            'detalles': forms.Textarea(attrs={'placeholder': 'Detalles'}),
        }

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        error_messages = {
            'username': {
                'required': 'Este campo es obligatorio.',
                'invalid': 'Nombre de usuario o contraseña incorrectos.'
            },
            'password': {
                'required': 'Este campo es obligatorio.',
            }
        }
        
        

    

    



