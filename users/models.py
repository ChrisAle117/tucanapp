import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('dueño', 'Dueño'),
        ('admin', 'Administrador'),
        ('entrenador', 'Entrenador'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    username = models.CharField(max_length=45, unique=True)

    token = models.CharField(max_length=255, blank=True, null=True)
    
    email = models.EmailField(unique=True, null=False)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=50)
    rol = models.CharField(max_length=10, choices=ROLES)
    detalles = models.TextField(blank=True, null=True)

    join_date = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','nombre', 'apellidos', 'rol']

    def __str__(self):
        return self.username
