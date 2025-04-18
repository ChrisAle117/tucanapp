from django.urls import path, include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'api', JugadorViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('jugadores/<int:pk>/', jugador_list, name='jugador-detail'),
]
