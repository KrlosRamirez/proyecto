# Generated by Django 5.1.2 on 2024-11-20 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Medicamentos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registromedicamento',
            name='nombrecitolulu',
            field=models.CharField(default='lulu', max_length=20),
        ),
    ]