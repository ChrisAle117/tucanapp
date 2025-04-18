from django.urls import path, include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'api', EventoViewSet, basename='eventos')

urlpatterns = [
    path('', include(router.urls)),
    path('equipo/<int:pk>/', evento_list, name='evento_list'),
]
