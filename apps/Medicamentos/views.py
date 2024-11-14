from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import inlineformset_factory
from .models import Benefactor, Medicamento, Destinatario, Entrega, EntregaItem, Proveedor, Donante, Insumo, Bitacora
from .forms import (
    MedicamentoForm,
    RegistroForm,
    CustomAuthenticationForm,
    DestinatarioForm,
    EntregaForm,
    EntregaItemForm,
    BaseEntregaItemFormSet,
    ProveedorForm,
    DonanteForm,
    InsumoForm,
    Bitacora,
    BenefactorForm,
)
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
import csv

from ..Utils.mensajes import *

function = Function()


#Incio de la app logueada.



def Inicio(request):
    return render(request, 'panel.html', {
    })




#-------------------------------------------------------------------------------------#




@login_required
@user_passes_test(lambda u: u.is_staff)
def bitacora(request):
    destinatario_id = request.GET.get('destinatario')
    if destinatario_id:
        registros = Bitacora.objects.filter(destinatario__id=destinatario_id).order_by('-fecha')
    else:
        registros = Bitacora.objects.all().order_by('-fecha')
    destinatarios = Destinatario.objects.all()
    return render(request, 'medicamentos/bitacora.html', {
        'registros': registros,
        'destinatarios': destinatarios,
        'destinatario_id': destinatario_id,
    })
def agregar_entrega(request):
    if request.method == 'POST':
        form = EntregaForm(request.POST)
        items_formset = EntregaItemForm(request.POST)
        if form.is_valid() and items_formset.is_valid():
            entrega = form.save()
            items_formset.instance = entrega
            items_formset.save()
            messages.success(request, 'Entrega registrada exitosamente.')
            # Registrar en la Bitácora
            Bitacora.objects.create(
                usuario=request.user,
                accion='Entrega registrada',
                descripcion=f'Se registró una entrega a {entrega.destinatario.nombre} {entrega.destinatario.apellido}.',
                destinatario=entrega.destinatario
            )
            return redirect('entregas')
    else:
        form = EntregaForm()
        items_formset = EntregaItemForm()
    return render(request, 'medicamentos/entrega_form.html', {'form': form, 'items_formset': items_formset})

@login_required
def exportar_bitacora_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="bitacora.pdf"'
    p = canvas.Canvas(response)

    # Agregar contenido al PDF (puedes personalizarlo)
    p.drawString(100, 750, "Bitácora de Medicamentos")
    # Lógica adicional para extraer y mostrar registros en el PDF

    p.showPage()
    p.save()
    return response


@login_required
@user_passes_test(lambda u: u.is_staff)
def lista_donantes(request):
    donantes = Donante.objects.all()
    return render(request, 'medicamentos/donantes_list.html', {'donantes': donantes})

@login_required
@user_passes_test(lambda u: u.is_staff)
def agregar_donante(request):
    if request.method == 'POST':
        form = DonanteForm(request.POST)
        if form.is_valid():
            form.save()
            texto = function.mensaje("Donante","Donante registrado exitosamente","success")
            messages.add_message(request, messages.SUCCESS,texto)
            return redirect('medicamentos:lista_donantes')
    else:
        form = DonanteForm()
    return render(request, 'medicamentos/donante_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_donante(request, pk):
    donante = get_object_or_404(Donante, pk=pk)
    if request.method == 'POST':
        form = DonanteForm(request.POST, instance=donante)
        if form.is_valid():
            form.save()
            texto = function.mensaje("Donante","Registro modificado exitosamente","success")
            messages.add_message(request, messages.SUCCESS,texto)
            return redirect('medicamentos:lista_donantes')
    else:
        form = DonanteForm(instance=donante)
    return render(request, 'medicamentos/donante_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def lista_insumos(request):
    insumos = Insumo.objects.all()
    return render(request, 'medicamentos/insumos_list.html', {'insumos': insumos})

@login_required
@user_passes_test(lambda u: u.is_staff)
def agregar_insumo(request):
    if request.method == 'POST':
        form = InsumoForm(request.POST)
        if form.is_valid():
            insumo = form.save()  # Código generado automáticamente en el modelo
            Bitacora.objects.create(
                usuario=request.user,
                accion="Agregar Insumo",
                descripcion=f"Se agregó el insumo {insumo.descripcion} con código {insumo.codigo}."
            )
            messages.success(request, "Insumo registrado exitosamente.")
            return redirect('medicamentos:lista_insumos')
    else:
        form = InsumoForm()
    return render(request, 'medicamentos/insumo_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_insumo(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    if request.method == 'POST':
        form = InsumoForm(request.POST, instance=insumo)
        if form.is_valid():
            insumo = form.save()
            # Registrar en la Bitácora
            Bitacora.objects.create(
                usuario=request.user,
                accion="Editar Insumo",
                descripcion=f"Se editó el insumo {insumo.descripcion} con código {insumo.codigo}."
            )
            texto = function.mensaje("Insumo","Registro modificado exitosamente","success")
            messages.add_message(request, messages.SUCCESS,texto)
            return redirect('medicamentos:lista_insumos')
    else:
        form = InsumoForm(instance=insumo)
    return render(request, 'medicamentos/insumo_form.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            cedula = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=cedula, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Has iniciado sesión como {cedula}.')
                return redirect('index')
            else:
                messages.error(request, 'Cédula de Identidad o contraseña incorrectos.')
        else:
            messages.error(request, 'Cédula de Identidad o contraseña incorrectos.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'medicamentos/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

def registro(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False  # Cambia a True si deseas que el usuario sea administrador
            user.is_active = True
            user.save()
            cedula = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {cedula}.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
    else:
        form = RegistroForm()
    return render(request, 'medicamentos/registro.html', {'form': form})

@login_required
def index(request):
    return render(request, 'medicamentos/index.html')

from django.utils import timezone
from datetime import timedelta

@login_required
def lista_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    # Fecha actual y fecha dentro de 30 días
    today = timezone.now().date()
    today_plus_30 = today + timedelta(days=30)
    # Medicamentos con stock bajo
    low_stock_medicamentos = medicamentos.filter(cantidad__lte=10)
    # Medicamentos próximos a vencer
    about_to_expire_medicamentos = medicamentos.filter(fecha_vencimiento__lte=today_plus_30)
    return render(request, 'medicamentos/medicamentos_list.html', {
        'medicamentos': medicamentos,
        'low_stock_medicamentos': low_stock_medicamentos,
        'about_to_expire_medicamentos': about_to_expire_medicamentos,
        'today_plus_30': today_plus_30,
        'today': today,
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def agregar_medicamento(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            medicamento = form.save()  

            Bitacora.objects.create(
                usuario=request.user,
                accion="Agregar Medicamento",
                descripcion=f"Se agregó el medicamento {medicamento.nombre} con código {medicamento.codigo}."
            )
            texto = function.mensaje("Medicamento", "Medicamento registrado exitosamente", "success")
            messages.add_message(request, messages.SUCCESS, texto)
            return redirect('medicamentos:lista_medicamentos')
    else:
        form = MedicamentoForm()
    return render(request, 'medicamentos/medicamento_form.html', {'form': form})



@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_medicamento(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    if request.method == "POST":
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save() 
            texto = function.mensaje("Medicamento","Registro modificado exitosamente","success")
            messages.add_message(request, messages.SUCCESS,texto)
            return redirect('medicamentos:lista_medicamentos')
    else:
        form = MedicamentoForm(instance=medicamento)
    return render(request, 'medicamentos/medicamento_form.html', {"form":form,"medicamento":medicamento})



@login_required
@user_passes_test(lambda u: u.is_staff)
def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'medicamentos/proveedores_list.html', {'proveedores': proveedores})

@login_required
@user_passes_test(lambda u: u.is_staff)
def agregar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor agregado exitosamente.')
            return redirect('medicamentos:lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'medicamentos/proveedor_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            texto = function.mensaje("Proveedor","Registro modificado exitosamente","success")
            messages.add_message(request, messages.SUCCESS,texto)
            return redirect('medicamentos:lista_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'medicamentos/proveedor_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_medicamento(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    if request.method == 'POST':
        medicamento.delete()
        texto = function.mensaje("Medicamento","Registro eliminado exitosamente","success")
        messages.add_message(request, messages.SUCCESS,texto)
        return redirect('medicamentos:lista_medicamentos')
    return render(request, 'medicamentos/eliminar_medicamento.html', {'medicamento': medicamento})

@login_required
def historial(request):
    entregas = Entrega.objects.all()
    return render(request, 'medicamentos/historial.html', {'entregas': entregas})

@login_required
def entregas(request):
    search_query = request.GET.get('search', '')
    if search_query:
        entregas_list = Entrega.objects.filter(
            Q(codigo__icontains=search_query) |
            Q(destinatario__nombre__icontains=search_query) |
            Q(destinatario__apellido__icontains=search_query)
        )
    else:
        entregas_list = Entrega.objects.all()
    entregas_list = entregas_list.order_by('-fecha_entrega')
    paginator = Paginator(entregas_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'medicamentos/entregas_list.html', {
        'entregas': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'paginator': paginator,
    })

@login_required
def detalle_entrega(request, pk):
    entrega = get_object_or_404(Entrega, pk=pk)
    return render(request, 'medicamentos/detalle_entrega.html', {'entrega': entrega})

@login_required
@user_passes_test(lambda u: u.is_staff)
def agregar_entrega(request):
    EntregaItemFormSet = inlineformset_factory(
        Entrega,
        EntregaItem,
        form=EntregaItemForm,
        formset=BaseEntregaItemFormSet,
        extra=1,
        can_delete=True,
    )
    if request.method == 'POST':
        form = EntregaForm(request.POST)
        if form.is_valid():
            entrega = form.save(commit=False)
            formset = EntregaItemFormSet(request.POST, instance=entrega)
            if formset.is_valid():
                # Validar cantidades antes de guardar
                for form_item in formset:
                    medicamento = form_item.cleaned_data.get('medicamento')
                    cantidad = form_item.cleaned_data.get('cantidad')
                    if cantidad > medicamento.cantidad:
                        messages.error(
                            request,
                            f"No hay suficiente stock de {medicamento.nombre}. Disponible: {medicamento.cantidad}"
                        )
                        return render(request, 'medicamentos/entrega_form.html', {'form': form, 'formset': formset})
                entrega.save()
                formset.save()
                # Actualizar stock
                for item in entrega.items.all():
                    medicamento = item.medicamento
                    medicamento.cantidad -= item.cantidad
                    medicamento.save()
                messages.success(request, 'Entrega registrada exitosamente.')
                return redirect('medicamentos:entregas')
            else:
                messages.error(request, 'Por favor, corrige los errores en los medicamentos.')
        else:
            messages.error(request, 'Por favor, corrige los errores en la información de la entrega.')
            formset = EntregaItemFormSet(request.POST)
    else:
        form = EntregaForm()
        entrega = Entrega()
        formset = EntregaItemFormSet(instance=entrega)
    return render(request, 'medicamentos/entrega_form.html', {'form': form, 'formset': formset})

@login_required
@user_passes_test(lambda u: u.is_staff)
def agregar_destinatario(request):
    if request.method == 'POST':
        form = DestinatarioForm(request.POST)
        if form.is_valid():
            form.save()
            texto = function.mensaje("Destinatario","Destinatario registrado exitosamente","success")
            messages.add_message(request, messages.SUCCESS,texto)
            return redirect('medicamentos:lista_destinatarios')
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
    else:
        form = DestinatarioForm()
    return render(request, 'medicamentos/destinatario_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_destinatario(request, pk):
    destinatario = get_object_or_404(Destinatario, pk=pk)
    if request.method == 'POST':
        form = DestinatarioForm(request.POST, instance=destinatario)
        if form.is_valid():
            form.save()
            texto = function.mensaje("Destinatario","Registro modificado exitosamente","success")
            messages.add_message(request, messages.SUCCESS,texto)
            return redirect('medicamentos:lista_destinatarios')
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
    else:
        form = DestinatarioForm(instance=destinatario)
    return render(request, 'medicamentos/destinatario_form.html', {'form': form})

@login_required
def detalle_destinatario(request, pk):
    destinatario = get_object_or_404(Destinatario, pk=pk)
    return render(request, 'medicamentos/detalle_destinatario.html', {'destinatario': destinatario})

@login_required
def lista_destinatarios(request):
    destinatarios = Destinatario.objects.all()
    return render(request, 'medicamentos/destinatarios_list.html', {'destinatarios': destinatarios})

@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_destinatario(request, pk):
    destinatario = get_object_or_404(Destinatario, pk=pk)
    if request.method == 'POST':
        destinatario.delete()
        texto = function.mensaje("Destinatario","Registro eliminado exitosamente","success")
        messages.add_message(request, messages.SUCCESS,texto)
        return redirect('medicamentos:lista_destinatarios')    
    return render(request, 'medicamentos/eliminar_destinatario.html', {'destinatario': destinatario})


@login_required
def exportar_entregas_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="entregas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Código', 'Destinatario', 'Medicamento', 'Cantidad', 'Fecha de Entrega', 'Observaciones'])

    entregas = Entrega.objects.all()
    for entrega in entregas:
        for item in entrega.items.all():
            writer.writerow([
                entrega.codigo,
                entrega.destinatario.nombre,
                item.medicamento.nombre,
                item.cantidad,
                entrega.fecha_entrega,
                entrega.observaciones,
            ])


    return response

#####################################################################################################

@login_required
@user_passes_test(lambda u: u.is_staff)
def agregar_benefactor(request):
    if request.method == 'POST':
        form = BenefactorForm(request.POST)
        if form.is_valid():
            form.save()
            # Mensaje de éxito
            texto = "Benefactor registrado exitosamente."
            messages.success(request, texto)
            return redirect('medicamentos:lista_benefactores')
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
    else:
        form = BenefactorForm()

    return render(request, 'medicamentos/benefactor_form.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_benefactor(request, pk):
    benefactor = get_object_or_404(Benefactor, pk=pk)
    if request.method == 'POST':
        form = BenefactorForm(request.POST, instance=benefactor)
        if form.is_valid():
            form.save()
            # Mensaje de éxito
            texto = "Registro modificado exitosamente"
            messages.success(request, texto)
            return redirect('medicamentos:lista_benefactores')
        else:
            messages.error(request, 'Por favor, corrige los errores a continuación.')
    else:
        form = BenefactorForm(instance=benefactor)

    return render(request, 'medicamentos/benefactor_form.html', {'form': form})


@login_required
def detalle_benefactor(request, pk):
    benefactores = get_object_or_404(Benefactor, pk=pk)
    return render(request, 'medicamentos/detalle_benefactor.html', {'benefactores': benefactores})

@login_required
def lista_benefactores(request):  
    benefactores = Benefactor.objects.all()
    return render(request, 'medicamentos/benefactores_list.html', {'benefactores': benefactores})

@login_required
@user_passes_test(lambda u: u.is_staff)
def eliminar_benefactor(request, pk):
    benefactor = get_object_or_404(Benefactor, pk=pk)
    if request.method == 'POST':
        benefactor.delete()
        texto = "Registro eliminado exitosamente"
        messages.success(request, texto)
        return redirect('medicamentos:lista_benefactores')

    return render(request, 'medicamentos/eliminar_benefactor.html', {'benefactor': benefactor})