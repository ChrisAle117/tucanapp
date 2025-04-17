from .models import Evento
from rest_framework import serializers

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['id', 'nombre', 'fecha', 'equipo1', 'equipo2', 'puntos_equipo1', 'puntos_equipo2', 'resultado']

    def validate(self, data):
        if data['equipo1'].deporte != data['equipo2'].deporte:
            raise serializers.ValidationError("Los equipos deben ser del mismo deporte")
        if data['equipo1'] == data['equipo2']:
            raise serializers.ValidationError("Un equipo no puede jugar contra sí mismo")
        return data