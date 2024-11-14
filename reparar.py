


"""
# Editar de Jefe de Familia

class editar_Jefe(UpdateView):
    form_class=ModificarJefe
    model=Jefe_familia
    template_name = 'jefe_familia/Jefe_familia_form.html'

    def get_success_url(self):
        return reverse_lazy('Censo:List_jefes_familia')

    def get(self, request, *args, **kwargs):
        jefe_familia = get_object_or_404(Jefe_familia, pk=self.kwargs.get('jefe_id'))
        formatted_birthdate = jefe_familia.fecha_naci.strftime('%Y-%m-%d')
        form = self.form_class(instance=jefe_familia, initial={'fecha_naci': formatted_birthdate})
        return render(request, self.template_name, {'form': form})

    

    def post(self, request,*args,**kwargs):
        self.object=self.get_object
        form=self.form_class(request.POST)
        if form.is_valid():
            jefe_familia=form.save(commit=False)
            if Jefe_familia.objects.filter(cedula_jefe_familia = request.POST['cedula_jefe_familia']).exists():
                texto = function.mensaje("Jefe de Familia","Ya existe un Jefe de Familia  registrado con esta cedula","error")
                messages.add_message(request, messages.SUCCESS,texto)
                return redirect('Censo:List_jefes_familia')
            else:
                jefe_familia.save()
                texto = function.mensaje("Jefe de Familia","Jefe de Familia registrado exitosamente","success")
                messages.add_message(request, messages.SUCCESS,texto)
                return redirect('Censo:List_jefes_familia')
        else:
            return render(request, self.template_name, {'form':form})

"""




# Eliminar 

def Jefe_familia_Eliminar(request,pk):
    try:
        jefe_familia = Jefe_familia.objects.get(pk=pk)
        jefe_familia .delete()

        texto = function.mensaje("Jefe de Familia","Registro eliminado exitosamente","success")
        messages.add_message(request, messages.SUCCESS,texto)
        return redirect('Censo:List_jefes_familia')
    
    except:
        texto = function.mensaje("Jefe de Familia","No puede ser eliminado porque ya posee una Carga Familiar","error")
        messages.add_message(request, messages.SUCCESS,texto)
        return redirect('Censo:List_jefes_familia')


# ------------------------------------------------------------------------------------ #


"""
# Vista  completa  de  Integrante


# Crear Integrante

def integranteCreateView(request):
    if request.method == 'POST':
        form = IntegraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Censo:integrante')
    else:
        form = IntegraForm()
    return render(request,'integrante/integrante_form.html',{'form':form})








# Editar Integrante

class integranteUpdateView(UpdateView):
    form_class = IntegraForm
    model = Integrante
    template_name = 'integrante/Integrante_form.html'

    def get_success_url(self):
        return reverse_lazy('Censo:List_integrantes')

class integranteDeleteVieww(DeleteView):
    model = Integrante
    template_name = 'integrante/Integrante_form.html'

    def get_success_url(self):
        return reverse_lazy('Censo:List_integrantes')



def Integrante_Eliminar(request,pk):
    try:
        integrante = Integrante.objects.get(pk=pk)
        integrante .delete()

        texto = function.mensaje("Integrante","Registro eliminado exitosamente","success")
        messages.add_message(request, messages.SUCCESS,texto)
        return redirect('Censo:List_integrantes')
    
    except:
        texto = function.mensaje("Integrante","No puede ser eliminado porque ya posee un Jefe de Familia","error")
        messages.add_message(request, messages.SUCCESS,texto)
        return redirect('Censo:List_integrantes')
 


# ------------------------------------------------------------------------------------ #



# Vista  completa  de  Carga Familiar



# Listado de Carga Familiar

class CargaListView(ListView):
    template_name = 'jefe_familia/carga_list.html'
    def get(self, request, *args, **kwargs):
        jefe_familia = Jefe_familia.objects.get(pk=kwargs['pk'])
        carga_familiar = CargaFamiliar.objects.filter(jefe_familia=jefe_familia)
        print(carga_familiar)
        return render(request,self.template_name,{'object_list':carga_familiar})





# Editar de Carga Familiar

class Carga_familiarUpdateView(UpdateView):
    form_class = CargaForm
    model = CargaFamiliar
    template_name = 'integrante/Integrante_form.html'

    def get_success_url(self):
        return reverse_lazy('Censo:carga_list')




# Listado de Carga Familiar

class Carga_familiarDeleteVieww(DeleteView):
    model = CargaFamiliar
    template_name = 'integrante/Integrante_form.html'

    def get_success_url(self):
        return reverse_lazy('Censo:carga_list')
        


# ------------------------------------------------------------------------------------ #







# Vista  completa  de  Discapacidad



# Crear  Discapacidad

class DiscapacidadCreateView(CreateView):
    form_class=DiscapacidadForm
    model=Discapacidad
    template_name = 'discapacidad/discapacidad_form.html'
    
    def get_success_url(self):
        return reverse_lazy('Censo:discapacidad')
"""
"""


# Listado de  Discapacidad


class DiscapacidadListView(ListView):
    model=Discapacidad
    template_name = 'discapacidad/discapacidad_list.html'

    def get_context_data(self, **kwargs):
        context = super(DiscapacidadListView, self).get_context_data(**kwargs)
        context['object_list'] = []
        if self.request.GET.get('nombre_cilindro'):
            for object in self.object_list:
                if self.request.GET['nombre_cilindro'].lower() in object.nombre_cilindro.lower():
                    context['object_list'].append(object)
        else:
             context['object_list'] = self.object_list
        return context




# Editar de Discapacidad

class discapacidadUpdateView(UpdateView):
    form_class = DiscapacidadForm
    model = Discapacidad
    template_name = 'discapacidad/discapacidad_form.html'

    def get_success_url(self):
        return reverse_lazy('Censo:List_discapacidad')

class DiscapacidadDeleteVieww(DeleteView):
    model = Discapacidad
    template_name = 'discapacidad/discapacidad_form.html'

    def get_success_url(self):
        return reverse_lazy('Censo:List_discapacidad')
        

"""


# ------------------------------------------------------------------------------------ #




"""
# Vista  completa  de  Votante



# Crear Votante

class   VotanteCreateView(CreateView):
    form_class=VotanteForm
    model=Votante
    template_name = 'votante/votante_form.html'
    
    def get_success_url(self):
        return reverse_lazy('Censo:votante')



# Listado de Votante 

class VotanteListView(ListView):
    model=Votante
    template_name = 'votante/votante_list.html'

    def get_context_data(self, **kwargs):
        context = super(VotanteListView, self).get_context_data(**kwargs)
        context['object_list'] = []
        if self.request.GET.get('centro_votacion'):
            for object in self.object_list:
                if self.request.GET['centro_votacion'].lower() in object.centro_votacion.lower():
                    context['object_list'].append(object)
        else:
             context['object_list'] = self.object_list
        return context






# Editar de Votante


class VotanteUpdateView(UpdateView):
    form_class = VotanteForm
    model = Votante
    template_name = 'votante/votante_form.html'

    def get_success_url(self):
        return reverse_lazy('Censo:List_Votante')




# Eliminar de  Votante

class VotanteDeleteVieww(DeleteView):
    model = Votante
    template_name = 'votante/votante_form.html'

    def get_success_url(self):
        return reverse_lazy('Censo:List_Votante')
        
# ------------------------------------------------------------------------------------ #
"""