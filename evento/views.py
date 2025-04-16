from .models import Evento
from .serializers import EventoSerializer


from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    renderer_classes = [JSONRenderer]

    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['GET']:
            return []
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def listar_eventos(self, request):
        # Filtrar eventos finalizados
        eventos_finalizados = Evento.objects.filter(fecha__lte=now()).order_by('-fecha')[:10]
        # Filtrar eventos futuros
        proximos_eventos = Evento.objects.filter(fecha__gt=now()).order_by('fecha')[:10]

        # Serializar los datos
        eventos_finalizados_serializados = self.get_serializer(eventos_finalizados, many=True).data
        proximos_eventos_serializados = self.get_serializer(proximos_eventos, many=True).data

        # Retornar la respuesta
        return Response({
            'proximosEventos': proximos_eventos_serializados,
            'eventosFinalizados': eventos_finalizados_serializados
        })