from .models import Equipo
from rest_framework import serializers
from django.forms import ValidationError
import re

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'
        extra_kwargs = {
            'activo': {'default': True, 'required': False}  #
        }
    
    def validate_nombre(self, value):
        if not re.match(r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9\s]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras, números, espacios, acentos y la letra ñ.")
        return value

    def validate_descripcion(self, value):
        if value and not re.match(r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9\s.,]+$', value):
            raise serializers.ValidationError("La descripción solo puede contener letras, números, espacios, puntos, comas, acentos y la letra ñ.")
        return value
    def validate_ciudad(self, value):
        if not re.match(r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$', value):
            raise serializers.ValidationError("La ciudad solo puede contener letras, espacios, acentos y la letra ñ.")
        return value
    def validate(self, data):
        instance = Equipo(**data)
        try:
            instance.clean() 
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict) 
        return data