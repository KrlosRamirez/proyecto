from django.urls import path
from django.contrib import admin
from . import views
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.login_view, name='login'),
    path('bienvenido/',views.login_required(Inicio), name = 'bienvenido'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('index/', views.index, name='index'),
    path('medicamentos/', views.lista_medicamentos, name='lista_medicamentos'),
    path('medicamentos/agregar/', views.agregar_medicamento, name='agregar_medicamento'),
    path('medicamentos/<int:pk>/editar/', views.editar_medicamento, name='editar_medicamento'),
    path('medicamentos/<int:pk>/eliminar/', views.eliminar_medicamento, name='eliminar_medicamento'),
    path('medicamentos/registrar/', views.registrar_medicamento, name='registrar_medicamento'),
    path('medicamentos/lregistrar/', views.lista_regis_medicamentos, name='lista_regis_medicamentos'),
    path('medicamentos/registro/<int:pk>/editar/', views.editar_registro_medicamento, name='editar_registro_medicamento'),
    path('medicamentos/registro/<int:pk>/eliminar/', views.eliminar_registro_medicamento, name='eliminar_registro_medicamento'),
    # path('medicamentos/reporte/', views.reporte_registro_medicamentos, name='reporte_registro_medicamentos'),
    path('medicamentos/reporte/', views.reporte_registro_medicamentos, name='reporte_registro_medicamentos'),
    path('historial/', views.historial, name='historial'),
    path('historial/exportar/', views.exportar_entregas_csv, name='exportar_entregas_csv'),
    path('entregas/', views.entregas, name='entregas'),
    path('entregas/agregar/', views.agregar_entrega, name='agregar_entrega'),
    path('entregas/<int:pk>/', views.detalle_entrega, name='detalle_entrega'),
    path('destinatarios/', views.lista_destinatarios, name='lista_destinatarios'),
    path('destinatarios/agregar/', views.agregar_destinatario, name='agregar_destinatario'),
    path('destinatarios/<int:pk>/editar/', views.editar_destinatario, name='editar_destinatario'),
    path('destinatarios/<int:pk>/eliminar/', views.eliminar_destinatario, name='eliminar_destinatario'),
    path('destinatarios/<int:pk>/', views.detalle_destinatario, name='detalle_destinatario'),
    path('insumos/', views.lista_insumos, name='lista_insumos'),
    path('insumos/agregar/', views.agregar_insumo, name='agregar_insumo'),
    path('insumos/<int:pk>/editar/', views.editar_insumo, name='editar_insumo'),
    path('bitacora/', views.bitacora, name='bitacora'),
    path('exportar_bitacora_pdf/', views.exportar_bitacora_pdf, name='exportar_bitacora_pdf'),
    path('benefactor/', views.lista_benefactores, name='lista_benefactores'),
    path('benefactor/agregar/', views.agregar_benefactor, name='agregar_benefactor'),
    path('benefactor/editar/<int:pk>/', views.editar_benefactor, name='editar_benefactor'),
    path('benefactor/eliminar/<int:pk>/', views.eliminar_benefactor, name='eliminar_benefactor'),
    path('benefactor/<int:pk>/', views.detalle_benefactor, name='detalle_benefactor'),

    path('reporte/entregas/', views.generar_reporte_entregas, name='generar_reporte_entregas'),
    path('reporte/registro_medicamentos/', views.generar_reporte_registro_medicamentos, name='generar_reporte_registro_medicamentos'),
    path('reporte/bajo_stock/', views.reporte_bajo_stock, name='reporte_bajo_stock'),
    path('reporte/proximos_a_vencer/', views.reporte_proximos_a_vencer, name='reporte_proximos_a_vencer'),

]

