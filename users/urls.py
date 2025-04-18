from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

#Definir un router
router = SimpleRouter()
router.register(r'api',UserViewSet)


urlpatterns = [
    path('', include(router.urls)),

    #Este es el path para iniciar sesión
    #Es POST y espera que le mandemos email y password
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    #El siguiente path es para refrescar el token de sesión
    #(Si es que eso queremos porque podriamos iniciar sesión de nuevo simplemente)
    path('token/refresh/', TokenRefreshView.as_view(), name='Token_refresh'),
    #Path para registrar un nuevo usuario
    path('registrar/', CustomUserFormAPI.as_view() , name='register'),

    path('dashboard/', dashboard, name='dashboard'),
    #URLS para envio y recuperación de contraseña
    path("send-reset-email/", send_reset_email, name="send_reset_email"),
    path("reset-password/", reset_password, name="reset_password"),


]