
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.decorators import login_required
from ..Usuario.views  import *
from ..Usuario import *


urlpatterns = [
    path('login/',LoginView.as_view(), name = 'login'),
    path('add/',login_required(UsersCreateView.as_view()), name = 'add'),
    path('',login_required(UserListView.as_view()), name = 'list'),
    path('accounts/login/',login_required(error404.as_view()), name = 'ERROR_404'),
    path('editar_usuario/<int:pk>/',login_required(UserUpdateView.as_view()), name = 'update_user'),
    path('delete/<int:pk>/',login_required(UserDeleteView.as_view()), name = 'delete_users'),
    path('perfil/',login_required(PerfilView.as_view()), name = 'perfil'),
    path('Actualizar/',login_required(actualizar_informacionView.as_view()), name = 'Actualizar'),
    path('update_notificaciones/',login_required(UpdateNotificaciones.as_view()), name = 'update_notificaciones'),
    path('ver_Usua/<int:pk>/',login_required(verusuario.as_view()), name = 'ver_Usuario'),


    
]         







