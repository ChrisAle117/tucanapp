from django.db import models, transaction

from deporte.models import Deporte

class ConfiguracionDeporte(models.Model):
    deporte = models.OneToOneField(
        Deporte,
        on_delete=models.CASCADE,
        primary_key=True
    )
    max_titulares = models.IntegerField()
    max_suplentes = models.IntegerField()
    
    def __str__(self):
        return f"{self.deporte}"
    