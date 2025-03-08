from django.db import models
from django.forms import ValidationError

from deporte.models import Deporte
from usuario.models import Usuario

class Equipo(models.Model):
    nombre = models.CharField(max_length=45, unique=True)
    logo_url = models.URLField(max_length=200, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=45)
    entrenador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipos_entrenados'
    )
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    num_titulares = models.IntegerField(default=0)
    num_suplentes = models.IntegerField(default=0)
    
    def clean(self):
        if self.entrenador and self.entrenador.rol != 'entrenador':
            raise ValidationError('El usuario asignado no es un entrenador')
    
    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"
