# Generated by Django 5.1.6 on 2025-04-15 05:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('deporte', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45, unique=True)),
                ('logo_url', models.URLField(blank=True, null=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('ciudad', models.CharField(max_length=45)),
                ('num_titulares', models.IntegerField(default=0)),
                ('num_suplentes', models.IntegerField(default=0)),
                ('deporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deporte.deporte')),
                ('entrenador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipos_entrenados', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
