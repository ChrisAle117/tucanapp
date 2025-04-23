from .models import ConfiguracionDeporte
from rest_framework import serializers
from deporte.models import Deporte
from deporte.serializers import DeporteSerializer


class ConfiguracionDeporteSerializer(serializers.ModelSerializer):
    deporte = DeporteSerializer()

    class Meta:
        model = ConfiguracionDeporte
        fields = '__all__'
    
    def validate_max_titulares(self, value):

        if value < 0:
            raise serializers.ValidationError("El número máximo de titulares no puede ser negativo.")
        return value

    def validate_max_suplentes(self, value):

        if value < 0:
            raise serializers.ValidationError("El número máximo de suplentes no puede ser negativo.")
        return value
    
    def create(self, validated_data):
        deporte_data = validated_data.pop('deporte')
        deporte = Deporte.objects.create(**deporte_data)
        configuracion_deporte = ConfiguracionDeporte.objects.create(deporte=deporte, **validated_data)
        return configuracion_deporte
    
    def update(self, instance, validated_data):
        deporte_data = validated_data.pop('deporte', None)

        if deporte_data:
            deporte_instance = instance.deporte
            for attr, value in deporte_data.items():
                setattr(deporte_instance, attr, value)
            deporte_instance.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance