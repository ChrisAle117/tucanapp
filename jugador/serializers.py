from .models import Jugador
from rest_framework import serializers
from datetime import date as Date, timedelta
import re
from .models import Jugador

class JugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jugador
        fields = '__all__'

    def validate_nombre(self, value):

        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras y espacios.")
        return value

    def validate_edad(self, value):

        if value < 0:
            raise serializers.ValidationError("La edad no puede ser negativa.")
        return value

    def validate_fecha_nacimiento(self, value):
        
        if value > Date.today():
            raise serializers.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        
        
        edad_minima = 15
        fecha_limite = Date.today() - timedelta(days=edad_minima * 365)  
        if value > fecha_limite:
            raise serializers.ValidationError("El jugador debe tener al menos 15 años.")
        
        return value

    def validate(self, data):

        if data['posicion'].deporte != data['equipo'].deporte:
            raise serializers.ValidationError("La posición no corresponde al deporte del equipo.")

        equipo = data['equipo']
        es_titular = data['es_titular']

        configuracion_deporte = equipo.deporte.configuraciondeporte

        titulares_actuales = Jugador.objects.filter(equipo=equipo, es_titular=True).count()
        suplentes_actuales = Jugador.objects.filter(equipo=equipo, es_titular=False).count()

        if es_titular and titulares_actuales >= configuracion_deporte.max_titulares:
            raise serializers.ValidationError(f"El equipo ya tiene el máximo de {configuracion_deporte.max_titulares} jugadores titulares.")
        if not es_titular and suplentes_actuales >= configuracion_deporte.max_suplentes:
            raise serializers.ValidationError(f"El equipo ya tiene el máximo de {configuracion_deporte.max_suplentes} jugadores suplentes.")

        return data