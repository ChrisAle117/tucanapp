from django.db import models
from django.core.exceptions import ValidationError

class Deporte(models.Model):
    nombre = models.CharField(max_length=45)
    
    def __str__(self):
        return self.nombre
    
    def clean(self):
        print(f"Validando en modelo deportes {self}")
        # Validar que el nombre sea único}
        if self.pk is None:
            # Caso de creación
            if Deporte.objects.filter(nombre=self.nombre).exists():
                raise ValidationError({"nombre": "Ya existe un deporte con este nombre."})
        else:
            # Caso de actualización
            if Deporte.objects.filter(nombre=self.nombre).exclude(pk=self.pk).exists():
                raise ValidationError({"nombre": "Ya existe un deporte con este nombre en otro registro."})
        
    def save(self, *args, **kwargs):
        # Llamar a clean antes de guardar
        self.clean()
        super().save(*args, **kwargs)
    
    def update(self, *args, **kwargs):
        # Llamar a clean antes de actualizar
        self.clean()
        super().save(*args, **kwargs)
    
