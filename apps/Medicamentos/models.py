from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils import timezone
import re
from django.core.validators import RegexValidator
from ..Usuario.models import *


class Benefactor(models.Model):
    TIPOS = [
        ('persona', 'Persona Natural'),
        ('comercio', 'Comercio'),
    ]

    codigo = models.CharField(max_length=50, unique=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    nombre = models.CharField(max_length=50)
    cedula = models.CharField(max_length=10, blank=True, null=True, unique=True)
    rif = models.CharField(max_length=12, blank=True, null=True, unique=True)
    direccion = models.TextField()
    telefono = models.CharField(max_length=11,
        validators=[RegexValidator(regex=r'^\d{7,11}$', message='El teléfono solo puede contener entre 7 y 11 números.')]
    )  
    email = models.EmailField(blank=True, null=True, unique=True) 

    def save(self, *args, **kwargs):
        if not self.codigo:
            ultimo_benefactor = Benefactor.objects.filter(codigo__regex=r'^\d+$').order_by('-codigo').first()
            nuevo_codigo = int(ultimo_benefactor.codigo) + 1 if ultimo_benefactor else 1
            self.codigo = str(nuevo_codigo).zfill(5)

        super().save(*args, **kwargs)

    def clean(self):
        # Validaciones cruzadas
        if self.tipo == 'persona' and not self.cedula:
            raise ValidationError({'cedula': 'La cédula es obligatoria para Persona Natural.'})
        if self.tipo == 'comercio' and not self.rif:
            raise ValidationError({'rif': 'El RIF es obligatorio para Comercio.'})

        # Validaciones de unicidad en instancias existentes
        if self.cedula and Benefactor.objects.filter(cedula=self.cedula).exclude(pk=self.pk).exists():
            raise ValidationError({'cedula': 'La cédula ya está registrada.'})

        if self.rif and Benefactor.objects.filter(rif=self.rif).exclude(pk=self.pk).exists():
            raise ValidationError({'rif': 'El RIF ya está registrado.'})

        if self.telefono and Benefactor.objects.filter(telefono=self.telefono).exclude(pk=self.pk).exists():
            raise ValidationError({'telefono': 'El teléfono ya está registrado.'})

        if self.email and Benefactor.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': 'El correo electrónico ya está registrado.'})

        super().clean()

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
    




class Proveedor(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.TextField()
    telefono = models.CharField(max_length=11)
    email = models.EmailField(unique=True)

    def clean(self):
        super().clean()
        if not self.email.lower().endswith('@gmail.com'):
            raise ValidationError({'email': 'El correo electrónico debe ser una dirección de Gmail.'})

    def __str__(self):
        return self.nombre

class Medicamento(models.Model):
    TIPO_CHOICES = [
        ('Genérico', 'Genérico'),
        ('Comercial', 'Comercial'),
    ]

    codigo = models.CharField(max_length=50, unique=True, blank=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    cantidad = models.PositiveIntegerField()
    fecha_vencimiento = models.DateField()
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, null=True, blank=True)
    tipo_medicamento = models.CharField(max_length=10, choices=TIPO_CHOICES)
    componentes = models.TextField()
    concentracion = models.CharField(max_length=100)
    fecha_produccion = models.DateField()

    def save(self, *args, **kwargs):
        if not self.codigo:

            ultimo_medicamento = Medicamento.objects.filter(codigo__regex=r'^\d+$').order_by('-codigo').first()
            if ultimo_medicamento:
                nuevo_codigo = int(ultimo_medicamento.codigo) + 1
            else:
                nuevo_codigo = 1  
            self.codigo = str(nuevo_codigo).zfill(5)  
        super().save(*args, **kwargs)

    def __str__(self):
        return f" {self.nombre} - {self.codigo}"



class Destinatario(models.Model):

    cedula_identidad = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    direccion = models.TextField()
    telefono = models.CharField(max_length=19)

    def __str__(self):
        return f"{self.cedula_identidad} - {self.nombre}"

class Entrega(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    destinatario = models.ForeignKey(Destinatario, on_delete=models.CASCADE)
    fecha_entrega = models.DateField()
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Entrega {self.codigo} a {self.destinatario.nombre}"

class EntregaItem(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE, related_name='items')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.medicamento.nombre} en {self.entrega.codigo}"

class Donante(models.Model):
    codigo = models.CharField(
        max_length=9,
        unique=True,
        validators=[
            RegexValidator(
                regex='^\d+$',
                message='La cédula debe contener solo números.',
                code='invalid_cedula'
            ),
        ]
    )
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion = models.TextField()
    telefono = models.CharField(max_length=9)

    def __str__(self):
        return f"{self.codigo} - {self.nombre} {self.apellido}"

class Insumo(models.Model):
    codigo = models.CharField(max_length=50, unique=True, blank=True)
    descripcion = models.TextField()
    cantidad = models.PositiveIntegerField()
    fecha_recepcion = models.DateField()
    donante = models.ForeignKey(Donante, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.codigo:
            ultimo_insumo = Insumo.objects.filter(codigo__regex=r'^\d+$').order_by('-codigo').first()
            if ultimo_insumo:
                nuevo_codigo = int(ultimo_insumo.codigo) + 1
            else:
                nuevo_codigo = 1
            self.codigo = str(nuevo_codigo).zfill(5)  # Código de 5 dígitos
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"


class Bitacora(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=200)
    descripcion = models.TextField()
    destinatario = models.ForeignKey(Destinatario, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.fecha} - {self.accion}"

from django.db import models

#_____________________________________________________________________________________________


