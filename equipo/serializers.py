from .models import Equipo
from rest_framework import serializers
from django.forms import ValidationError
import re

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'
        extra_kwargs = {
            'activo': {'default': True, 'required': False}  # Valor predeterminado y no obligatorio
        }
    
    def validate_nombre(self, value):

        if not re.match(r'^[a-zA-Z0-9\s]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras, números y espacios.")
        return value

    def validate_descripcion(self, value):
        # Validar que la descripción no contenga caracteres especiales (si no está vacía)
        if value and not re.match(r'^[a-zA-Z0-9\s.,]+$', value):
            raise serializers.ValidationError("La descripción solo puede contener letras, números, espacios, puntos y comas.")
        return value

    def validate_ciudad(self, value):
        # Validar que la ciudad no contenga caracteres especiales
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("La ciudad solo puede contener letras y espacios.")
        return value
    
    def validate(self, data):
        # Crea una instancia temporal para validar
        instance = Equipo(**data)
        try:
            instance.clean()  # Llama a las validaciones del modelo
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)  # Convierte los errores a JSON
        return data