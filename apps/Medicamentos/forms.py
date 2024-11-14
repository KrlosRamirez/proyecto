from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Medicamento, Destinatario, Entrega, EntregaItem, Donante, Insumo, Proveedor, Bitacora, Benefactor
import datetime
from django.core.exceptions import ValidationError

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Cédula de Identidad',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }
        help_texts = {
            'username': 'Ingrese su Cédula de Identidad sin puntos ni guiones.',
            'password1': None,
            'password2': None,
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.isdigit():
            raise forms.ValidationError('La Cédula de Identidad debe contener solo números.')
        if len(username) < 7 or len(username) > 9:
            raise forms.ValidationError('La Cédula de Identidad debe tener entre 7 y 9 dígitos.')
        return username

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Cédula de Identidad'
        self.fields['username'].help_text = 'Ingrese su Cédula de Identidad sin puntos ni guiones.'

class DonanteForm(forms.ModelForm):
    class Meta:
        model = Donante
        fields = ['codigo', 'nombre', 'apellido', 'direccion', 'telefono']
        labels = {
            'codigo': 'Cédula',
            'nombre': 'Nombres',
            'apellido': 'Apellidos',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
        }

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['descripcion', 
                  'cantidad', 
                  'fecha_recepcion', 
                  'donante']
        labels = {
            'descripcion': 'Descripción',
            'cantidad': 'Cantidad',
            'fecha_recepcion': 'Fecha de Recepción',
            'donante': 'Donante',
        }

        widgets = {
            'fecha_recepcion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def clean_fecha_recepcion(self):
        fecha = self.cleaned_data['fecha_recepcion']
        if fecha > datetime.date.today():
            raise forms.ValidationError('La fecha de recepción no puede ser futura.')
        return fecha

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = [
            'id',
            'nombre',
            'descripcion',
            'cantidad',
            'fecha_vencimiento',
            'benefactor',
            'tipo_medicamento',
            'componentes',
            'concentracion',
            'fecha_produccion',
        ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'cantidad': 'Cantidad',
            'fecha_vencimiento': 'Fecha de Vencimiento',
            'benefactor': 'Benefactor',
            'tipo_medicamento': 'Tipo de Medicamento',
            'componentes': 'Componentes',
            'concentracion': 'Concentración',
            'fecha_produccion': 'Fecha de Producción',
        }
        widgets = {
            'fecha_vencimiento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_produccion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(MedicamentoForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['fecha_vencimiento'].initial = self.instance.fecha_vencimiento
            self.fields['fecha_produccion'].initial = self.instance.fecha_produccion



    def clean_fecha_vencimiento(self):
        fecha_vencimiento = self.cleaned_data['fecha_vencimiento']
        if fecha_vencimiento <= datetime.date.today():
            raise forms.ValidationError('La fecha de vencimiento debe ser futura.')
        return fecha_vencimiento

    def clean_fecha_produccion(self):
        fecha_produccion = self.cleaned_data['fecha_produccion']
        if fecha_produccion > datetime.date.today():
            raise forms.ValidationError('La fecha de producción no puede ser futura.')
        return fecha_produccion

class DestinatarioForm(forms.ModelForm):
    class Meta:
        model = Destinatario
        fields = ['cedula_identidad', 'nombre', 'fecha_nacimiento', 'direccion', 'telefono']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'cedula_identidad': 'Cédula de Identidad',
            'nombre': 'Nombre',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
        }
        widgets = {
            'fecha_nacimiento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['codigo', 'destinatario', 'fecha_entrega', 'observaciones']
        widgets = {
            'codigo':forms.NumberInput(attrs = {'class':'form-control','id':'codigo'}),
            'destinatario': forms.Select(attrs={'class':'form-control','id':'destinatario'}),
            'observaciones':forms.TextInput(attrs = {'class':'form-control','id':'direccion'}),
            'fecha_entrega':forms.DateInput(format=('%d-%m-%Y'),attrs={'id':'hasta','class':'form-control','type':'date'} ),

        }
        labels = {
            'codigo': 'Código de Entrega',
            'destinatario': 'Destinatario',
            'fecha_entrega': 'Fecha de Entrega',
            'observaciones': 'Observaciones',
        }

class EntregaItemForm(forms.ModelForm):
    class Meta:
        model = EntregaItem
        fields = ['medicamento', 'cantidad']
        widgets = {
            'medicamento': forms.Select(attrs={'class':'form-control','id':'destinatario'}),
            'cantidad':forms.NumberInput(attrs = {'class':'form-control','id':'codigo'}),

        }
        labels = {
            'medicamento': 'Medicamento',
            'cantidad': 'Cantidad',
        }

class BaseEntregaItemFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                medicamento = form.cleaned_data.get('medicamento')
                cantidad = form.cleaned_data.get('cantidad')
                if cantidad > medicamento.cantidad:
                    raise forms.ValidationError(
                        f"No hay suficiente stock de {medicamento.nombre}. Disponible: {medicamento.cantidad}"
                    )
                



class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono', 'direccion', 'email']
        labels = {
            'nombre': 'Nombres',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
        }
        widgets = {
        'nombre':forms.TextInput(attrs = {'class':'form-control','id':'nombre'}),
        'telefono':forms.NumberInput(attrs={'class':'form-control','placeholder':'Introduzca Telefono','validate':'NUMEROS,ENTER,ESPACIO','minlength':'8','maxlength':'8'}),
        'direccion':forms.TextInput(attrs = {'class':'form-control','id':'direccion'}),
        'email':forms.EmailInput(attrs = {'class':'form-control','id':'email'})

         }

class BitacoraForm(forms.ModelForm):
    class Meta:
        model = Bitacora
        fields = '__all__'


#_____________________________________________________________________________________________

class BenefactorForm(forms.ModelForm):
    class Meta:
        model = Benefactor
        fields = [
            'codigo',
            'tipo',
            'nombre',
            'cedula',
            'rif',
            'direccion',
            'telefono',
            'email',
        ]
        labels = {
            'codigo': 'Código',
            'tipo': 'Tipo de Benefactor',
            'nombre': 'Nombre',
            'cedula': 'Cédula',
            'rif': 'RIF',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
        }
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ingrese la dirección'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese Teléfono'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese Correo Electrónico'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'placeholder': 'Ingrese Cédula'}),
            'rif': forms.TextInput(attrs={'placeholder': 'Ingrese RIF'}),
            'codigo': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(BenefactorForm, self).__init__(*args, **kwargs)
        # Ajustes para campos específicos
        self.fields['cedula'].required = False
        self.fields['rif'].required = False

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        tipo = self.cleaned_data.get('tipo')

        if tipo == 'persona' and not cedula:
            raise ValidationError('La cédula es obligatoria para Personas Naturales.')

        # Validar unicidad
        if cedula and Benefactor.objects.filter(cedula=cedula).exclude(pk=self.instance.pk).exists():
            raise ValidationError('La cédula ya está registrada.')

        return cedula

    def clean_rif(self):
        rif = self.cleaned_data.get('rif')
        tipo = self.cleaned_data.get('tipo')

        if tipo == 'comercio' and not rif:
            raise ValidationError('El RIF es obligatorio para Comercios.')

        # Validar unicidad
        if rif and Benefactor.objects.filter(rif=rif).exclude(pk=self.instance.pk).exists():
            raise ValidationError('El RIF ya está registrado.')

        return rif

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Validar unicidad
        if email and Benefactor.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('El correo electrónico ya está registrado.')

        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')

        # Validar unicidad
        if telefono and Benefactor.objects.filter(telefono=telefono).exclude(pk=self.instance.pk).exists():
            raise ValidationError('El teléfono ya está registrado.')

        return telefono

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        cedula = cleaned_data.get('cedula')
        rif = cleaned_data.get('rif')

        # Validación cruzada entre cedula y rif
        if tipo == 'persona' and not cedula:
            self.add_error('cedula', 'La cédula es obligatoria para Personas Naturales.')
        elif tipo == 'comercio' and not rif:
            self.add_error('rif', 'El RIF es obligatorio para Comercios.')

        return cleaned_data