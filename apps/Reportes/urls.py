from django.urls import path
from .views  import *
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path('censo_p/',login_required(Censo_p.as_view()), name = 'censo_p'),
    path('productos_p/',login_required(Productos_p.as_view()), name = 'productos_p'),
    path('asigna_p/',login_required(Asigna_p.as_view()), name = 'asigna_p'),
    path('pago_p/',login_required(Pago_p.as_view()), name = 'pago_p'),
    path('entrega_p/',login_required(Entrega_p.as_view()), name = 'entrega_p'),
    path('detalles_p/<int:pk>',login_required(DetaleBolsa_p.as_view()), name = 'detalle_p'),


]