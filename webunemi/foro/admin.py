from django.contrib import admin
from .models import Publicacion
'''from .models import Usuario

# Register your models here.
admin.site.register(Usuario)'''
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.unregister(User)
admin.site.register(User, BaseUserAdmin)

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_publicacion', 'activo')
    list_filter = ('activo', 'fecha_publicacion')
    search_fields = ('titulo', 'contenido')
    list_editable = ('activo',)
    fields = ('titulo', 'contenido', 'html_contenido', 'fecha_publicacion', 'activo', 'imagen')
    readonly_fields = ('fecha_publicacion',)