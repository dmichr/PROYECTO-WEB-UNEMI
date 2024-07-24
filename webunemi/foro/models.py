from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models

def unemi_email_validator(value):
    if not value.endswith('@unemi.edu.ec'):
        raise ValidationError(
            _('%(value)s is not a valid UNEMI email'),
            params={'value': value},
        )
#gfuncion para validar solo correos unemi



class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='images/')  
    html_contenido = models.FileField(upload_to='html_files/',blank=True, null=True)  # Campo para contenido HTML adicional

    def __str__(self):
        return self.titulo
