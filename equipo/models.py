from django.db import models
from django.forms import ValidationError

from deporte.models import Deporte
from configuracion_deporte.models import ConfiguracionDeporte
from users.models import CustomUser as Usuario

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
    
    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    def clean(self):
        errors = {}
        if self.entrenador and self.entrenador.rol != 'entrenador':
            errors['entrenador'] = 'El usuario asignado no es un entrenador'
        if self.num_titulares < 0 or self.num_suplentes < 0:
            errors['num_titulares'] = 'El número de titulares y suplentes no puede ser negativo'
        if self.num_titulares > ConfiguracionDeporte.objects.get(deporte=self.deporte).max_titulares:
            errors['num_titulares'] = 'El número de titulares excede el máximo permitido'
        if self.num_suplentes > ConfiguracionDeporte.objects.get(deporte=self.deporte).max_suplentes:
            errors['num_suplentes'] = 'El número de suplentes excede el máximo permitido'

        if errors:
            raise ValidationError(errors)
    
    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"
