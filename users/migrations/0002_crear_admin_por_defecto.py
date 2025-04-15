from django.db import migrations
from django.contrib.auth.hashers import make_password
import os


def crear_admin(apps, schema_editor):
    """
    Crea un usuario administrador por defecto si no existe.
    """
    CustomUser = apps.get_model('users', 'CustomUser')

    # Leer valores desde variables de entorno o usar valores predeterminados
    ADMIN_USERNAME = os.environ.get('DJANGO_ADMIN_USERNAME', 'admin')
    ADMIN_EMAIL = os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@gmail.com')
    ADMIN_PASSWORD = os.environ.get('DJANGO_ADMIN_PASSWORD', 'admin123')  # Cambiar en producción
    ADMIN_NOMBRE = os.environ.get('DJANGO_ADMIN_NOMBRE', 'Admin')
    ADMIN_APELLIDOS = os.environ.get('DJANGO_ADMIN_APELLIDOS', 'Principal')

    try:
        # Verificar si el usuario ya existe
        if not CustomUser.objects.filter(username=ADMIN_USERNAME).exists():
            # Crear el usuario administrador
            CustomUser.objects.create(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password=make_password(ADMIN_PASSWORD),
                nombre=ADMIN_NOMBRE,
                apellidos=ADMIN_APELLIDOS,
                rol='admin',
                is_superuser=True,
                is_staff=True,
                is_active=True,
            )
            print(f"Usuario administrador '{ADMIN_USERNAME}' creado exitosamente.")
        else:
            print(f"El usuario administrador '{ADMIN_USERNAME}' ya existe. No se creó un duplicado.")
    except Exception as e:
        print(f"Error al crear el usuario administrador: {e}")
        raise e


def eliminar_admin(apps, schema_editor):
    """
    Elimina el usuario administrador por defecto si existe.
    """
    CustomUser = apps.get_model('users', 'CustomUser')
    ADMIN_USERNAME = os.environ.get('DJANGO_ADMIN_USERNAME', 'admin')

    try:
        admin_user = CustomUser.objects.filter(username=ADMIN_USERNAME).first()
        if admin_user and admin_user.is_superuser:
            admin_user.delete()
            print(f"Usuario administrador '{ADMIN_USERNAME}' eliminado exitosamente.")
        else:
            print(f"El usuario '{ADMIN_USERNAME}' no existe o no es un superusuario. No se eliminó nada.")
    except Exception as e:
        print(f"Error al eliminar el usuario administrador: {e}")
        raise e


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_admin, eliminar_admin),
    ]