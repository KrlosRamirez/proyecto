from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Medicamento, Destinatario, Entrega, EntregaItem, Insumo, Bitacora, Benefactor, RegistroMedicamento
import datetime
from django.core.exceptions import ValidationError

#____________________________________________________________________________________________________________

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

#____________________________________________________________________________________________________________

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Cédula de Identidad'
        self.fields['username'].help_text = 'Ingrese su Cédula de Identidad sin puntos ni guiones.'

#____________________________________________________________________________________________________________

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['descripcion', 
                  'cantidad', 
                  'fecha_recepcion', 
                  'benefactor']
        labels = {
            'descripcion': 'Descripción',
            'cantidad': 'Cantidad',
            'fecha_recepcion': 'Fecha de Recepción',
            'benefactor': 'Benefactor',
        }

        widgets = {
            'fecha_recepcion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def clean_fecha_recepcion(self):
        fecha = self.cleaned_data['fecha_recepcion']
        if fecha > datetime.date.today():
            raise forms.ValidationError('La fecha de recepción no puede ser futura.')
        return fecha

#____________________________________________________________________________________________________________

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = [
            'id',
            'nombre',
            'descripcion',
            'tipo_medicamento',
            'tipo_farmac',
            'componentes',
            'concentracion',
        ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'fecha_vencimiento': 'Fecha de Vencimiento',
            'componentes': 'Componentes',
            'concentracion': 'Concentración',
            'tipo_farmac' : 'Forma farmaceutica',
        }
        widgets = {

        }

class RegistroMedicamentoForm(forms.ModelForm):
    class Meta:
        model = RegistroMedicamento
        fields = [
            'medicamento',
            'benefactor',
            'produccion_tanda',
            'vencimiento_tanda',
            'cantidad',
        ]
        labels = {
            'medicamento': 'Medicamento',
            'benefactor': 'Benefactor',
            'produccion_tanda': 'fecha de produccion',
            'vencimiento_tanda': 'fecha de venciento',
            'cantidad': 'Cantidad'
        }
        widgets = {
            'vencimiento_tanda': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'produccion_tanda': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(RegistroMedicamentoForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['vencimiento_tanda'].initial = self.instance.vencimiento_tanda
            self.fields['produccion_tanda'].initial = self.instance.produccion_tanda


    def clean_vencimiento_tanda(self):
        vencimiento_tanda = self.cleaned_data['vencimiento_tanda']
        if vencimiento_tanda <= datetime.date.today():
            raise forms.ValidationError('La fecha de vencimiento debe ser futura.')
        return vencimiento_tanda

    def clean_produccion_tanda(self):
        produccion_tanda = self.cleaned_data['produccion_tanda']
        if produccion_tanda > datetime.date.today():
            raise forms.ValidationError('La fecha de producción no puede ser futura.')
        return produccion_tanda

#____________________________________________________________________________________________________________

class DestinatarioForm(forms.ModelForm):
    class Meta:
        model = Destinatario
        fields = [
            'tipo_n',
            'cedula_identidad', 
            'nombre',     
            'apellido',
            'fecha_nacimiento', 
            'direccion', 
            'telefono',
        ]
        
        widgets = {
            'fecha_nacimiento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
        labels = {
            'tipo_n': 'Nacionalidad',
            'cedula_identidad': 'Documento de Identidad',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
        }

    def __init__(self, *args, **kwargs):
        super(DestinatarioForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['fecha_nacimiento'].initial = self.instance.fecha_nacimiento

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
        edad = (datetime.date.today() - fecha_nacimiento).days // 365
        if edad < 18:
            raise forms.ValidationError('El destinatario debe ser mayor de 18 años.')
        return fecha_nacimiento

    def clean_cedula_identidad(self):
        cedula_identidad = self.cleaned_data['cedula_identidad']
        if Destinatario.objects.filter(cedula_identidad=cedula_identidad).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('El documento de identidad ya está registrado.')
        return cedula_identidad

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if Destinatario.objects.filter(telefono=telefono).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('El telefono ya está registrado.')
        if not telefono.isdigit():
            raise forms.ValidationError('El teléfono debe contener solo números.')
        if len(telefono) < 10 or len(telefono) > 15:
            raise forms.ValidationError('El teléfono debe tener entre 10 y 15 dígitos.')
        return telefono

#____________________________________________________________________________________________________________

class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = [
            'destinatario', 
            'observaciones',
            ]
        labels = {
            'destinatario': 'Beneficiario',
            'observaciones': 'Observaciones',
            
        }
        widgets = {
            'destinatario': forms.Select(attrs={'class':'form-control','id':'destinatario'}),
            'observaciones':forms.TextInput(attrs = {'class':'form-control','id':'direccion'}),
        }

class EntregaItemForm(forms.ModelForm):
    class Meta:
        model = EntregaItem
        fields = [
            'medicamento', 
            'cantidad',
            'benefactor',
            'lote'
            ]
        widgets = {
            'medicamento': forms.Select(attrs={'class':'form-control','id':'destinatario'}),
            'cantidad':forms.NumberInput(attrs = {'class':'form-control','id':'cantidad'}),
            'benefactor' :  forms.Select(attrs={'class':'form-control','id':'benefactor'}),

        }
        labels = {
            'medicamento': 'Medicamento',
            'cantidad': 'Cantidad',
            'benefactor': 'Benefactor',
            'lote' : 'Lote de medicamento'
        }

#____________________________________________________________________________________________________________

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

#____________________________________________________________________________________________________________

class BitacoraForm(forms.ModelForm):
    class Meta:
        model = Bitacora
        fields = '__all__'

#____________________________________________________________________________________________________________

class BenefactorForm(forms.ModelForm):
    class Meta:
        model = Benefactor
        fields = [
            'codigo',
            'tipo',
            'tipo_p',
            'tipo_rif',
            'nombre',
            'apellido',
            'cedula',
            'rif',
            'direccion',
            'telefono',
            'email',
        ]
        labels = {
            'codigo': 'Código',
            'tipo': 'Tipo de Benefactor',
            'tipo_p': 'Nacionalidad',
            'tipo_rif': 'Tipo de Comercio',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'cedula': 'Cédula',
            'rif': 'RIF',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ingrese la dirección'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese Teléfono'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese Correo Electrónico'}),
            'nombre' :forms.TextInput(attrs = {'placeholder':'Nombre'}),
            'apellido' :forms.TextInput(attrs = {'placeholder':'Apellido'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'placeholder': 'Ingrese Cédula'}),
            'rif': forms.TextInput(attrs={'placeholder': 'Ingrese RIF'}),
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