# Generated by Django 5.1.1 on 2024-10-31 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='paciente',
            field=models.CharField(max_length=255),
        ),
    ]