# Generated by Django 5.1.2 on 2024-11-13 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Medicamentos', '0002_alter_benefactor_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destinatario',
            name='telefono',
            field=models.CharField(max_length=19),
        ),
    ]
