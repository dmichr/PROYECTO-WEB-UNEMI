from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Usuario

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        help_text='Requerido. 30 caracteres o menos. Solo letras, dígitos y @/./+/-/_.',
        label='Nombre de Usuario'
    )
    contraseña = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        help_text='Requerido. Tu contraseña no puede ser demasiado similar a tu otra información personal. Debe contener al menos 8 caracteres y no ser completamente numérica.'
    )
    
    nombre = forms.CharField(max_length=100, required=True, label='Nombre')
    email = forms.EmailField(required=True, label='Correo Electrónico')
    

    class Meta:
        model = User
        fields = ['username', 'nombre',  'email',  'contraseña', ]


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

            usuario, created = Usuario.objects.get_or_create(
                user=user,
                defaults={
                    'nombre': self.cleaned_data['nombre'],
                    'correo': self.cleaned_data['correo'],  
                }
            )
            
            if not created:
                usuario.nombre = self.cleaned_data['nombre']
                usuario.email = self.cleaned_data['correo']
                usuario.save()

        return user


class LoginForm(AuthenticationForm):
    class Meta:
        model = AuthenticationForm
        fields = ['usuario', 'contraseña']
