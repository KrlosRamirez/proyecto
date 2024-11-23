from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils import timezone
import re
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from ..Usuario.models import *


class Benefactor(models.Model):
    TIPOS = [
        ('persona', 'Persona Natural'),
        ('comercio', 'Comercio'),
    ]
    TIPOS_P = [
        ('V', 'V'),
        ('E', 'E'),
    ]
    TIPOS_RIF = [
        ('G', 'G'),
        ('I', 'I'),
    ]

    codigo = models.CharField(max_length=50, unique=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    tipo_p = models.CharField(max_length=1, choices=TIPOS_P, blank=True, null=True)
    tipo_rif = models.CharField(max_length=1, choices=TIPOS_RIF, blank=True, null=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    cedula = models.CharField(
        max_length=10,
        blank=True, null=True, unique=True,
        validators=[
            MinLengthValidator(8, message='La cédula debe tener al menos 8 dígitos.'),
            MaxLengthValidator(10, message='La cédula debe tener como máximo 10 dígitos.'),
            RegexValidator(regex='^\d+$', message='La cédula debe contener solo números.')
        ]
    )
    rif = models.CharField(
        max_length=12, blank=True, null=True, unique=True,
        validators=[
            RegexValidator(regex='^\d+$', message='El RIF debe contener solo números.')
        ]
    )
    direccion = models.TextField()
    telefono = models.CharField(
        max_length=11,
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
        campos_a_validar = {
            'cedula': self.cedula,
            'rif': self.rif,
            'telefono': self.telefono,
            'email': self.email,
        }

        for campo, valor in campos_a_validar.items():
            if valor and Benefactor.objects.filter(**{campo: valor}).exclude(pk=self.pk).exists():
                raise ValidationError({campo: f'El {campo} ya está registrado.'})

        super().clean()

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

#____________________________________________________________________________________________________________

class Medicamento(models.Model):
    TIPO_CHOICES = [
        ('Genérico', 'Genérico'),
        ('Comercial', 'Comercial'),
    ]
    TIPOS_FARMAC = [
        ('Tabletas','Tabletas'),
        ('Capsulas','Capsulas'),
        ('Jarabes','Jarabes'),
        ('Soluciones','Soluciones'),
        ('Gotas orales','Gotas orales'),
        ('Cremas','Cremas'),
        ('Inyectables','Inyectables'),
        ('Supositorios','Supositorios'),
        ('Otros','Otros'),
    ]
    codigo = models.CharField(max_length=50, unique=True, blank=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    cantidad = models.PositiveIntegerField(default=0)  
    tipo_medicamento = models.CharField(max_length=10, choices=TIPO_CHOICES)
    tipo_farmac = models.CharField(max_length=20, choices=TIPOS_FARMAC)
    componentes = models.TextField()
    concentracion = models.CharField(max_length=100)

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

class RegistroMedicamento(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, null=True, blank=True)
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, null=True, blank=True)
    fecha_registro_medicamento = models.DateField(auto_now_add=True)
    produccion_tanda = models.DateField()
    vencimiento_tanda = models.DateField()
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.pk} - Unidades disponibles: {self.cantidad}'

#____________________________________________________________________________________________________________

class Destinatario(models.Model):
    TIPOS_N = [
        ('V', 'V'),
        ('E', 'E'),
    ]
    tipo_n = models.CharField(max_length=1, choices=TIPOS_N)
    cedula_identidad = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            MinLengthValidator(8, message='La cédula debe tener al menos 8 dígitos.'),
            MaxLengthValidator(10, message='La cédula debe tener como máximo 10 dígitos.'),
            RegexValidator(regex='^\d+$', message='La cédula debe contener solo números.')
        ]
    )
    nombre = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='El nombre debe contener solo letras y espacios.')
        ]
    )
    apellido = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message='El apellido debe contener solo letras y espacios.')
        ]
    )
    fecha_nacimiento = models.DateField()
    direccion = models.TextField()
    telefono = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            MinLengthValidator(7, message='El teléfono debe tener al menos 7 dígitos.'),
            MaxLengthValidator(11, message='El teléfono debe tener como máximo 11 dígitos.'),
            RegexValidator(regex='^\d+$', message='El teléfono debe contener solo números.')
        ]
    )

    def clean(self):
        # Validar que la fecha de nacimiento no sea futura
        if self.fecha_nacimiento:
            if self.fecha_nacimiento > timezone.now().date():
                raise ValidationError({'fecha_nacimiento': 'La fecha de nacimiento no puede ser en el futuro.'})
        else:
            raise ValidationError({'fecha_nacimiento': 'Este campo es obligatorio.'})

    def __str__(self):
        return f"{self.cedula_identidad} - {self.nombre}"

#____________________________________________________________________________________________________________

class Entrega(models.Model):
    destinatario = models.ForeignKey(Destinatario, on_delete=models.CASCADE)
    fecha_entrega = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Entrega {self.pk} a {self.destinatario.nombre}"

    def clean(self):
        # Validar que el destinatario exista
        if not self.destinatario:
            raise ValidationError("El destinatario es obligatorio.")
        
        # Validar observaciones no demasiado largas (opcional)
        if self.observaciones and len(self.observaciones) > 500:
            raise ValidationError("Las observaciones no pueden superar los 500 caracteres.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Entrega(models.Model):
    
    destinatario = models.ForeignKey(Destinatario, on_delete=models.CASCADE)
    fecha_entrega = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)
    
    

    def __str__(self):
        return f"Entrega {self.pk} a {self.destinatario.nombre}"

#____________________________________________________________________________________________________________

class EntregaItem(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE, related_name='items')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, null=True, blank=True)
    lote = models.ForeignKey(RegistroMedicamento, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.cantidad} x {self.medicamento.nombre} en {self.entrega.codigo}"

    def clean(self):
        # Validar que la cantidad sea mayor a 0
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0.")
        
        # Validar que el medicamento esté disponible en suficiente cantidad
        if self.medicamento.cantidad < self.cantidad:
            raise ValidationError(f"No hay suficiente stock para el medicamento {self.medicamento.nombre}.")
        
        # Validar que el lote pertenece al medicamento
        if self.lote.medicamento != self.medicamento:
            raise ValidationError("El lote seleccionado no corresponde al medicamento.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class EntregaItem(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE, related_name='items')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, null=True, blank=True)
    
    lote = models.ForeignKey(RegistroMedicamento, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.cantidad} x {self.medicamento.nombre} en {self.entrega.codigo}"

#____________________________________________________________________________________________________________

class Insumo(models.Model):
    codigo = models.CharField(max_length=50, unique=True, blank=True)
    descripcion = models.TextField()
    cantidad = models.PositiveIntegerField()
    fecha_recepcion = models.DateField()
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            ultimo_insumo = Insumo.objects.filter(codigo__regex=r'^\d+$').order_by('-codigo').first()
            if ultimo_insumo:
                nuevo_codigo = int(ultimo_insumo.codigo) + 1
            else:
                nuevo_codigo = 1
            self.codigo = str(nuevo_codigo).zfill(5)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

#____________________________________________________________________________________________________________

class Bitacora(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=200)
    descripcion = models.TextField()
    destinatario = models.ForeignKey(Destinatario, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.fecha} - {self.accion}"

from django.db import models


