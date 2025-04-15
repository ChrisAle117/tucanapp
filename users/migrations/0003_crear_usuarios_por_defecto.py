from django.db import migrations
from django.contrib.auth.hashers import make_password
import os


def crear_usuarios_por_defecto(apps, schema_editor):
    """
    Crea un usuario dueño y un entrenador por defecto si no existen.
    """
    CustomUser = apps.get_model('users', 'CustomUser')

    # Leer valores desde variables de entorno o usar valores predeterminados
    DUENO_USERNAME = os.environ.get('DJANGO_DUENO_USERNAME', 'dueno')
    DUENO_EMAIL = os.environ.get('DJANGO_DUENO_EMAIL', 'dueno@example.com')
    DUENO_PASSWORD = os.environ.get('DJANGO_DUENO_PASSWORD', 'dueno123')  # Cambiar en producción
    DUENO_NOMBRE = os.environ.get('DJANGO_DUENO_NOMBRE', 'Dueño')
    DUENO_APELLIDOS = os.environ.get('DJANGO_DUENO_APELLIDOS', 'Principal')

    ENTRENADOR_USERNAME = os.environ.get('DJANGO_ENTRENADOR_USERNAME', 'entrenador')
    ENTRENADOR_EMAIL = os.environ.get('DJANGO_ENTRENADOR_EMAIL', 'entrenador@example.com')
    ENTRENADOR_PASSWORD = os.environ.get('DJANGO_ENTRENADOR_PASSWORD', 'entrenador123')  # Cambiar en producción
    ENTRENADOR_NOMBRE = os.environ.get('DJANGO_ENTRENADOR_NOMBRE', 'Entrenador')
    ENTRENADOR_APELLIDOS = os.environ.get('DJANGO_ENTRENADOR_APELLIDOS', 'Deportivo')

    try:
        # Crear usuario dueño si no existe
        if not CustomUser.objects.filter(username=DUENO_USERNAME).exists():
            CustomUser.objects.create(
                username=DUENO_USERNAME,
                email=DUENO_EMAIL,
                password=make_password(DUENO_PASSWORD),
                nombre=DUENO_NOMBRE,
                apellidos=DUENO_APELLIDOS,
                rol='presidente',
                is_superuser=False,
                is_staff=True,
                is_active=True,
            )
            print(f"Usuario dueño '{DUENO_USERNAME}' creado exitosamente.")
        else:
            print(f"El usuario dueño '{DUENO_USERNAME}' ya existe. No se creó un duplicado.")

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
    DUENO_USERNAME = os.environ.get('DJANGO_DUENO_USERNAME', 'dueno')
    ENTRENADOR_USERNAME = os.environ.get('DJANGO_ENTRENADOR_USERNAME', 'entrenador')

    try:
        # Eliminar usuario dueño
        dueno_user = CustomUser.objects.filter(username=DUENO_USERNAME).first()
        if dueno_user:
            dueno_user.delete()
            print(f"Usuario dueño '{DUENO_USERNAME}' eliminado exitosamente.")
        else:
            print(f"El usuario dueño '{DUENO_USERNAME}' no existe. No se eliminó nada.")

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