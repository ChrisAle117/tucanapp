from .models import Evento
from rest_framework import serializers
from equipo.models import Equipo, Deporte
import re


from rest_framework import serializers
from .models import Evento

class EventoSerializer(serializers.ModelSerializer):
    deporte_nombre = serializers.CharField(source='deporte.nombre', read_only=True)
    resultado_equipo = serializers.SerializerMethodField()
    class Meta:
        model = Evento
        fields = '__all__'

    def validate(self, data):
        if data['equipo1'].deporte != data['equipo2'].deporte:
            raise serializers.ValidationError("Los equipos deben ser del mismo deporte")
        if data['equipo1'] == data['equipo2']:
            raise serializers.ValidationError("Un equipo no puede jugar contra sí mismo")
        return data
    
     
    def validate_nombre(self, value):
        if not re.match(r'^[a-zA-Z0-9\s]+$', value):
            raise serializers.ValidationError("El nombre del evento solo puede contener letras, números y espacios.")
        return value
    def validate_puntos_equipo1(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Los puntos del equipo 1 no pueden ser negativos.")
        return value
    def validate_puntos_equipo2(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Los puntos del equipo 2 no pueden ser negativos.")
        return value

    def get_resultado_equipo(self, obj):
        equipo_id = self.context.get('equipo_id') 
        if not equipo_id:
            return None
        if obj.puntos_equipo1 is None or obj.puntos_equipo2 is None:
                return "Resultado pendiente"

        if obj.equipo1.id == equipo_id:
                if obj.puntos_equipo1 > obj.puntos_equipo2:
                    return "Victoria"
                elif obj.puntos_equipo1 < obj.puntos_equipo2:
                    return "Derrota"
                else:
                    return "Empate"
        elif obj.equipo2.id == equipo_id:
                if obj.puntos_equipo2 > obj.puntos_equipo1:
                    return "Victoria"
                elif obj.puntos_equipo2 < obj.puntos_equipo1:
                    return "Derrota"
                else:
                    return "Empate"
        return None
