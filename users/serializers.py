from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['rol'] = user.rol
        
        return token
    
    
    def validate(self, attrs):
        username_or_email = attrs.get("email")  
        password = attrs.get("password")
        
        # Buscar usuario por username o email
        user = CustomUser.objects.filter(email=username_or_email).first()
        if not user:
            user = CustomUser.objects.filter(username=username_or_email).first()

        if user and user.check_password(password):
            self.user = user
        else:
            raise serializers.ValidationError("Credenciales inválidas")
        
        attrs["username"] = self.user.username
        attrs["email"] = self.user.email

        data = super().validate(attrs)

        data["id"] = self.user.id
        data["rol"] = self.user.rol

        return data



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    

