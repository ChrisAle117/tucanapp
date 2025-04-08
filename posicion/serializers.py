from .models import Posicion
from rest_framework import serializers

class PosicionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posicion
        fields = '__all__'
        