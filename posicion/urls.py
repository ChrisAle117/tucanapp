# posicion/urls.py
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PosicionViewSet

router = SimpleRouter()
router.register(r'api', PosicionViewSet)

urlpatterns = router.urls
