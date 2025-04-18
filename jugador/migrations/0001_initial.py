# Generated by Django 5.1.6 on 2025-04-15 05:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('equipo', '__first__'),
        ('posicion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('edad', models.IntegerField()),
                ('fecha_nacimiento', models.DateField()),
                ('puntaje_mvp', models.FloatField(blank=True, null=True)),
                ('es_titular', models.BooleanField(default=False)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipo.equipo')),
                ('posicion', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='posicion.posicion')),
            ],
        ),
    ]
