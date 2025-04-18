from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Jugador
from .serializers import JugadorSerializer

class JugadorViewSet(viewsets.ModelViewSet):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer
    renderer_classes = [JSONRenderer]

    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['GET','POST','PUT', 'DELETE']:
            return [IsAuthenticated()]
        return []

from rest_framework.decorators import api_view, permission_classes, authentication_classes

@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(['GET'])
def jugador_list(request, pk):
    jugadores = Jugador.objects.filter(equipo=pk)
    serializer = JugadorSerializer(jugadores, many=True)
    return Response({'jugadores': serializer.data}, status=200)