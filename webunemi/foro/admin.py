from django.contrib import admin
from .models import Publicacion, Carrusell, Boletin, Evento
from django.core.exceptions import ValidationError
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
'''from .models import Usuario

# Register your models here.
admin.site.register(Usuario)'''
from django import forms





@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_publicacion', 'activo')
    list_filter = ('activo', 'fecha_publicacion')
    search_fields = ('titulo', 'contenido')
    list_editable = ('activo',)
    fields = ('titulo', 'contenido', 'html_contenido', 'fecha_publicacion', 'activo', 'imagen')
    readonly_fields = ('fecha_publicacion',)
    
    

class CarrusellForm(forms.ModelForm):
    class Meta:
        model = Carrusell
        fields = '__all__'

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if not imagen:
            raise forms.ValidationError('Debe seleccionar una imagen.')
        return imagen


class CarrusellAdmin(admin.ModelAdmin):
    form = CarrusellForm
    list_display = ('titulo', 'fecha_subida', 'activo', 'imagen', 'link')
    list_filter = ('activo', 'fecha_subida')
    search_fields = ('titulo',)

    def save_model(self, request, obj, form, change):
        if not change and not obj.imagen:  # Si es un nuevo objeto y no hay imagen
            form.add_error('imagen', 'Debe seleccionar una imagen.')
            return
        try:
            obj.full_clean()
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    form.add_error(field, error)
            return
        super().save_model(request, obj, form, change)

    # Prevención del envío del formulario al presionar "Enter"


    def render_change_form(self, request, context, *args, **kwargs):
        response = super().render_change_form(request, context, *args, **kwargs)
        
        if isinstance(response, TemplateResponse):
            script = """
            <script>
            document.addEventListener('DOMContentLoaded', function() {
                var form = document.querySelector('form');
                form.querySelectorAll('input[type="text"], input[type="url"]').forEach(function(input) {
                    input.addEventListener('keypress', function(event) {
                        if (event.keyCode == 13) {
                            event.preventDefault();
                            return false;
                        }
                    });
                });
            });
            </script>
            """
            response.content = mark_safe(response.rendered_content + script)
        
        return response
admin.site.register(Carrusell, CarrusellAdmin)

@admin.register(Boletin)
class BoletinAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'enlace')
    list_filter = ('fecha',)
    search_fields = ('titulo', 'fecha')
    date_hierarchy = 'fecha'
    
    
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location')
    search_fields = ('title', 'description')
