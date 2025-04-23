from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from deporte.models import Deporte
from configuracion_deporte.models import ConfiguracionDeporte
from users.models import CustomUser as Usuario
from django.utils import timezone
from django.db.models import Q


def validate_image_size(value):
    # Limitar el tamaño del archivo a 5 MB (5 * 1024 * 1024 bytes)
    limit = 5 * 1024 * 1024  # 5 MB en bytes
    if value.size > limit:
        raise ValidationError('El tamaño del archivo no puede ser mayor a 5 MB.')

class Equipo(models.Model):
    nombre = models.CharField(max_length=45, unique=True)
    logo = models.ImageField(
        upload_to='logos_equipos/', 
        blank=True, 
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png']),
            validate_image_size
        ]
    )  
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
    activo = models.BooleanField(default=True) 
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Llama al método clean antes de guardar
        super().save(*args, **kwargs)

    def clean(self):
        errors = {}

        if self.entrenador and self.entrenador.rol != 'entrenador':
            errors['entrenador'] = 'El usuario asignado no es un entrenador'

        if self.num_titulares < 0 or self.num_suplentes < 0:
            errors['num_titulares'] = 'El número de titulares y suplentes no puede ser negativo'

        try:
            config = ConfiguracionDeporte.objects.get(deporte=self.deporte)
            if self.num_titulares > config.max_titulares:
                errors['num_titulares'] = f'No puedes tener más de {config.max_titulares} titulares'
            if self.num_suplentes > config.max_suplentes:
                errors['num_suplentes'] = f'No puedes tener más de {config.max_suplentes} suplentes'
        except ConfiguracionDeporte.DoesNotExist:
            errors['deporte'] = 'No existe configuración para este deporte'

        if not self.activo:
            from evento.models import Evento  # Importar aquí para evitar dependencias circulares
        
            # Verificar si el equipo ya está guardado en la base de datos
            if self.pk:  # Solo realizar la validación si el equipo ya tiene un ID
                eventos_futuros = Evento.objects.filter(
                    (Q(equipo1=self) | Q(equipo2=self)) & Q(fecha__gte=timezone.now())
                )
                if eventos_futuros.exists():
                    errors['activo'] = 'No puedes desactivar un equipo con eventos futuros'
        

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f"{self.nombre} ({self.ciudad})"
