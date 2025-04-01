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

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        class_='mb-3 form-control',
        type='text',
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
        strip=False,
    )
    password = forms.CharField(
        class_='mb-3 form-control',
        type='password',
        placeholder='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )
    error_messages = {
        'invalid_login': {
            'message': 'Nombre de usuario o contraseña incorrectos.',
        },
        'inactive': {
            'message': 'Esta cuenta está inactiva.',
        },
    }
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        }

    def clean(self):
        super().clean()
        if self.cleaned_data.get('username') == '':
            raise forms.ValidationError('El nombre de usuario es obligatorio.')
        if self.cleaned_data.get('password') == '':
            raise forms.ValidationError('La contraseña es obligatoria.')
        return self.cleaned_data
    




