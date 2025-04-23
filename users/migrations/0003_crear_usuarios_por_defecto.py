from django.db import migrations
from django.contrib.auth.hashers import make_password
import os


def crear_usuarios_por_defecto(apps, schema_editor):
    """
    Crea un usuario dueño y un entrenador por defecto si no existen.
    """
    CustomUser = apps.get_model('users', 'CustomUser')


    ENTRENADOR_USERNAME = os.environ.get('DJANGO_ENTRENADOR_USERNAME', 'entrenador')
    ENTRENADOR_EMAIL = os.environ.get('DJANGO_ENTRENADOR_EMAIL', 'entrenador@example.com')
    ENTRENADOR_PASSWORD = os.environ.get('DJANGO_ENTRENADOR_PASSWORD', 'entrenador123')  # Cambiar en producción
    ENTRENADOR_NOMBRE = os.environ.get('DJANGO_ENTRENADOR_NOMBRE', 'Entrenador')
    ENTRENADOR_APELLIDOS = os.environ.get('DJANGO_ENTRENADOR_APELLIDOS', 'Deportivo')

    try:
        # Crear usuario entrenador si no existe
        if not CustomUser.objects.filter(username=ENTRENADOR_USERNAME).exists():
            CustomUser.objects.create(
                username=ENTRENADOR_USERNAME,
                email=ENTRENADOR_EMAIL,
                password=make_password(ENTRENADOR_PASSWORD),
                nombre=ENTRENADOR_NOMBRE,
                apellidos=ENTRENADOR_APELLIDOS,
                rol='entrenador',
                is_superuser=False,
                is_staff=False,
                is_active=True,
            )
            print(f"Usuario entrenador '{ENTRENADOR_USERNAME}' creado exitosamente.")
        else:
            print(f"El usuario entrenador '{ENTRENADOR_USERNAME}' ya existe. No se creó un duplicado.")
    except Exception as e:
        print(f"Error al crear los usuarios por defecto: {e}")
        raise e


def eliminar_usuarios_por_defecto(apps, schema_editor):
    """
    Elimina los usuarios dueño y entrenador por defecto si existen.
    """
    CustomUser = apps.get_model('users', 'CustomUser')
    ENTRENADOR_USERNAME = os.environ.get('DJANGO_ENTRENADOR_USERNAME', 'entrenador')

    try:
        
        # Eliminar usuario entrenador
        entrenador_user = CustomUser.objects.filter(username=ENTRENADOR_USERNAME).first()
        if entrenador_user:
            entrenador_user.delete()
            print(f"Usuario entrenador '{ENTRENADOR_USERNAME}' eliminado exitosamente.")
        else:
            print(f"El usuario entrenador '{ENTRENADOR_USERNAME}' no existe. No se eliminó nada.")
    except Exception as e:
        print(f"Error al eliminar los usuarios por defecto: {e}")
        raise e


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_crear_admin_por_defecto'),
    ]

    operations = [
        migrations.RunPython(crear_usuarios_por_defecto, eliminar_usuarios_por_defecto),
    ]