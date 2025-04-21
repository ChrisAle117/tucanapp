# posicion/urls.py
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PosicionViewSet, posiciones_deporte

router = SimpleRouter()
router.register(r'api', PosicionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('equipo/<int:pk>/', posiciones_deporte, name='posicion_list'),
]
