# Generated by Django 5.1.2 on 2024-11-20 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Medicamentos', '0003_rename_fecha_registro_registromedicamento_fecha_registro_medicamento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registromedicamento',
            name='nombrecitolulu',
        ),
    ]