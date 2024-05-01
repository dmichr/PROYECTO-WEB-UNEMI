from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

def unemi_email_validator(value):
    if not value.endswith('@unemi.edu.ec'):
        raise ValidationError(
            _('El correo electrónico debe ser de la extensión @unemi.edu.ec'),
            params={'value': value},
        )

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[unemi_email_validator])
    usuario = models.CharField(unique=True, max_length=15, validators=[
        MinLengthValidator(3, message="El nombre de usuario debe tener al menos 3 caracteres"),
        MaxLengthValidator(15, message="El nombre de usuario no puede tener más de 15 caracteres")
    ])
    contraseña = models.CharField(max_length=100)  # Asegúrate de cifrar la contraseña antes de guardarla
    
    def clean(self):
        # Llamar al clean de la superclase para asegurar que se realicen otras validaciones de campos
        super().clean()
        # Validar que el usuario sea igual al prefijo del correo electrónico
        if self.email and self.usuario:
            prefix, _, domain = self.email.partition('@')
            if prefix != self.usuario:
                raise ValidationError(
                    _('El usuario debe ser igual al prefijo del correo electrónico.'),
                    code='invalid'
                )

class Registro(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    # Agrega más campos según tus necesidades

