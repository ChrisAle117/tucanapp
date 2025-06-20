from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

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
            raise AuthenticationFailed("Credenciales inválidas")
        
        attrs["username"] = self.user.username
        attrs["email"] = self.user.email

        data = super().validate(attrs)

        data["id"]= self.user.id
        
        return data



class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = CustomUser
        fields = ['id' , 'nombre', 'apellidos', 'username', 'email', 'rol', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password) 
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

