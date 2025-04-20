from .models import Deporte
from rest_framework import serializers

class DeporteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = Deporte
        fields = '__all__'

    def create(self, validated_data):
        # Crear el objeto Deporte directamente, ya que las validaciones se manejan en validate
        deporte = Deporte.objects.create(**validated_data)
        return deporte

    def update(self, instance, validated_data):
        # Actualizar solo los campos que han cambiado
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
