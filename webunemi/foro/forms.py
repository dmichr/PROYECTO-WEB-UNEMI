from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
 
    username = forms.CharField(
        max_length=30,
        required=True,
        help_text='Requerido. 30 caracteres o menos. Solo letras, dígitos y @/./+/-/_.',
        label='Nombre de Usuario')
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        help_text='Requerido. Tu contraseña no puede ser demasiado similar a tu otra información personal. Debe contener al menos 8 caracteres y no ser completamente numérica.'
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput,
        help_text='Ingresa la misma contraseña de nuevo para verificar.'
    )
    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name',  'password1','password2', ]
	
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado')
        return email


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Las contraseñas no coinciden.')
        return password2
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user



