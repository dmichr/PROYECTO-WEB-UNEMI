from django.core.exceptions import ValidationError
#from django.utils.translation import gettext_lazy as _
from django.db import models
from PIL import Image,  UnidentifiedImageError

import io

'''def unemi_email_validator(value):
    if not value.endswith('@unemi.edu.ec'):
        raise ValidationError(
            _('%(value)s is not a valid UNEMI email'),
            params={'value': value},
        )
#gfuncion para validar solo correos unemi'''



class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)  
    html_contenido = models.FileField(upload_to='html_files/',blank=True, null=True)  # Campo para contenido HTML adicional

    def __str__(self):
        return self.titulo

#funcion para validar las dimensiones de las imagenes a cargar
def validate_image_dimensions(image):
    max_width = 1500
    max_height = 1200
    try:
        img = Image.open(image)
        img.verify()  # Verifica que es una imagen válida
        width, height = img.size
        if width > max_width or height > max_height:
            raise ValidationError(f'La imagen debe tener un tamaño máximo de {max_width}x{max_height} píxeles.')
    except UnidentifiedImageError:
        raise ValidationError('El archivo subido no es una imagen válida.')


#carrusell
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
        validate_image_dimensions(self.imagen)
    
    #para validar y redirigir imagenes con links (en caso el admin no suba link a una imagen)
    def get_link(self):
        return self.link if self.link and self.link.lower() != 'none' else None