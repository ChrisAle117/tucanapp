from django.db import models

from deporte.models import Deporte

class Posicion(models.Model):
    nombre = models.CharField(max_length=45)
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombre} ({self.deporte.nombre})"
    
    class constraints:
        unique_together = ('nombre', 'deporte')
