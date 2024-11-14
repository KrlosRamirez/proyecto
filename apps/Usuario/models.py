from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
import django
from django.utils import timezone
from ..Utils.selects import Selects
from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver



# Crea tus modelos aquí.


class UsersManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise ValueError('Las usuarios deben tener un nombre de usuario válido.')

        account = self.model(
            username=self.model.normalize_username(username)
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, username, password, **kwargs):
        account = self.create_user(username, password, **kwargs)

        account.is_superuser = True
        account.is_staff = True
        account.save()

        return account

class Users(AbstractBaseUser, PermissionsMixin):
    MANZANA_CHOICES = [
    ('Manzana 4', 'Manzana 4'),
    ('Manzana 8', 'Manzana 8'),


    ]
    username = models.CharField(_('Cedula'), max_length=40, unique=True)
    first_name = models.CharField(_('first name'), max_length=40)
    last_name = models.CharField(_('last name'), max_length=40)
    email = models.EmailField(_('Email'))
    is_admin = models.BooleanField(_('administrador'),  blank=True,default=False)
    is_usuario = models.BooleanField(_('manzaneros'),  blank=True,default=False)
    foto = models.ImageField(upload_to='images/login/')

    is_active= models.BooleanField(_('Active'), default=True)
    is_staff=models.BooleanField(_('Staff Status'), default=True)
    is_superuser=models.BooleanField(_('Superuser Status'), default=False)

    date_joined = models.DateTimeField(_('Sate Joined'), default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UsersManager()

    USERNAME_FIELD = 'username'


    def get_full_name(self):
        return ' '.join([self.username])

    def get_short_name(self):
        return self.first_name

    @classmethod
    def numeroRegistrados(self):
        return int(self.objects.all().count() )

    @classmethod
    def numeroUsuarios(self,tipo):
        if tipo == 'administrador':
            return int(self.objects.filter(is_superuser = True).count() )
        elif tipo == 'usuario':
            return int(self.objects.filter(is_superuser = False).count() )
    
    def __str__(self):
        return '{} {} {}'.format(self.username, self.first_name, self.last_name)




class Notificacion(models.Model):
    usuario= models.ForeignKey(Users,null=True,blank=True, on_delete = models.CASCADE)
    contenido = models.CharField(max_length=800)
    tip = (
        ("jefe de calle","jefe de calle"),
        ("administrador","administrador"),
    )
    url = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100, choices=tip)
    estatus = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '{} {}'.format(self.usuario,self.estatus)

    