from django.db import models
#creacion de los modelos-para bdd
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    usuario = models.CharField(unique=True,max_length=15)
    contraseña = models.CharField(max_length=100)

class Registro(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    # Agrega más campos según tus necesidades

