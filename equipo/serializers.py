from .models import Equipo
from rest_framework import serializers
from django.forms import ValidationError
class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'
    
    def validate(self, data):
        # Crea una instancia temporal para validar
        instance = Equipo(**data)
        try:
            instance.clean()  # Llama a las validaciones del modelo
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)  # Convierte los errores a JSON
        return data