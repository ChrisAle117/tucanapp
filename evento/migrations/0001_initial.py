# Generated by Django 5.1.7 on 2025-03-08 20:06

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('resultado', models.CharField(blank=True, max_length=45, null=True)),
                ('equipo1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos_como_equipo1', to='equipo.equipo')),
                ('equipo2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos_como_equipo2', to='equipo.equipo')),
            ],
        ),
    ]
