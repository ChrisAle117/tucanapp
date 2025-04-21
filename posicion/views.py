from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Posicion
from .serializers import PosicionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes

class PosicionViewSet(viewsets.ModelViewSet):
    queryset = Posicion.objects.all()
    serializer_class = PosicionSerializer
    renderer_classes = [JSONRenderer]

    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['GET','POST','PUT', 'DELETE']:
            return [IsAuthenticated()]
        return []

@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
@api_view(['GET'])
def posiciones_deporte(request, pk):
    if request.method == 'GET':
        queryset = Posicion.objects.filter(deporte_id=pk)
        serializer = PosicionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)