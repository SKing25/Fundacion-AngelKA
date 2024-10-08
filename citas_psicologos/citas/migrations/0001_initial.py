# Generated by Django 5.1.1 on 2024-09-17 20:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Psicologo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('paciente', models.CharField(max_length=100)),
                ('psicologo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citas.psicologo')),
            ],
            options={
                'unique_together': {('psicologo', 'fecha', 'hora')},
            },
        ),
    ]
