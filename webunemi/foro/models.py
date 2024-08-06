from django.core.exceptions import ValidationError
#from django.utils.translation import gettext_lazy as _
from django.db import models
from PIL import Image,  UnidentifiedImageError
from django.contrib.auth.models import AbstractUser
import io

'''def unemi_email_validator(value):
    if not value.endswith('@unemi.edu.ec'):
        raise ValidationError(
            _('%(value)s is not a valid UNEMI email'),
            params={'value': value},
        )
#gfuncion para validar solo correos unemi'''


class Boletin(models.Model):
    titulo = models.CharField(max_length=200)
    fecha = models.DateField()
    imagen = models.ImageField(upload_to='boletines/')
    enlace = models.URLField()

    def __str__(self):
        return f"{self.titulo} - {self.fecha}"

    class Meta:
        ordering = ['-fecha']



class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)  
    html_contenido = models.FileField(upload_to='html_files/',blank=True, null=True)  # Campo para contenido HTML adicional

    def __str__(self):
        return self.titulo

from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError

def validate_image_dimensions(image):
    if not image:
        return  # No validamos si no hay imagen
    max_width = 1500
    max_height = 1200
    try:
        img = Image.open(image)
        width, height = img.size
        if width > max_width or height > max_height:
            raise ValidationError(f'La imagen debe tener un tamaño máximo de {max_width}x{max_height} píxeles.')
    except UnidentifiedImageError:
        raise ValidationError('El archivo subido no es una imagen válida.')

class Carrusell(models.Model):
    titulo = models.CharField(max_length=200)
    fecha_subida = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='carousel_images/', validators=[validate_image_dimensions])
    link = models.URLField(blank=True, null=True) 
    
    def __str__(self):
        return self.titulo
    
    def clean(self):
        super().clean()
        if self.imagen:
            validate_image_dimensions(self.imagen)
    
    def get_link(self):
        return self.link if self.link and self.link.lower() != 'none' else None
    
#Modelo para eventos del calendario
class Evento(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    
