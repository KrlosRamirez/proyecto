from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, TemplateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.context import RequestContext
from ..Utils.mixins import AdminRequiredMixin,UsuarioRequiredMixin
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import *
from .models import *
from ..Utils.mensajes import *
from django import db
from ..Utils.mixins import AdminRequiredMixin, UsuarioRequiredMixin

db.connections.close_all()


# Crea tus vistas aquí.

function = Function()





class LoginView(View):
    form_class = AuthenticationForm
    template_name = "comun/login.html"


    def get(self, request):
        form = AuthenticationForm()
        return render(request, "comun/login.html", { 'form': form , 'message': ''})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                texto = function.mensaje("Inventario","Bienvenido al Sistema:                  "
                    + username,"success")
                messages.add_message(request, messages.SUCCESS,texto)
                url_next = request.GET.get('next')
                if url_next is not None:
                    return redirect(url_next)
                else:
                    return render(request,'preloader.html')
        else:
            mensaje = function.mensaje("Disculpe","Ingrese la cedula y la clave correcta.","warning")
            messages.add_message(request, messages.SUCCESS,mensaje)
        return render(request, self.template_name, {'form': self.form_class, 'message': mensaje})





class UsersCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    form_class = UsersModelForm
    model = Users
    template_name = 'administrador/users_form.html'
    success_url = '/'

    def form_valid(self, form):
        form = super(UsersCreateView, self).form_valid(form)
        texto = function.mensaje(
            "Usuario","El Usuario fue registrado exitosamente","success")
        messages.add_message(self.request, messages.SUCCESS, texto)
        return form


class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    context_object_name = 'list_user'
    model = Users
    template_name = 'administrador/listado_user.html'



class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    template_name = 'administrador/editar_usuario.html'
    model = Users
    fields = ['username','first_name','last_name','email']
    success_url = '/list/'


class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Users
    template_name = 'administrador/user_confirm_delete.html'
    success_url = reverse_lazy('usuarios:list')

# logout
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('/')

#########ERROR####################################################################3
class error404(TemplateView):
    template_name = 'login/page-error.html'


class PerfilView(LoginRequiredMixin, UsuarioRequiredMixin, TemplateView):
    template_name = 'login/perfil.html'
    def get(self,request):
        representante = representante.objects.filter(usuario=request.user)
        form = EditForm() # type: ignore
        return render(request,self.template_name,{'representante':representante,'form':form})


class actualizar_informacionView(LoginRequiredMixin,TemplateView):
    template_name = 'login/actualizar_informacion.html'
    def get(self,request):
        representante = representante.objects.filter(usuario=request.user)
        form = EditForm() # type: ignore
        return render(request,self.template_name,{'representante':representante,'form':form})


#Noficaciones
def Notificaciones(usuario,contenido,url,tipo):
    notificacion = Notificacion(usuario=usuario,contenido=contenido,url=url,tipo=tipo)
    notificacion.save()
    return True

def getNotifications(request):
    if request.user.is_secretaria:
        notificacion = Notificacion.objects.filter(tipo="secretaria")

    if request.user.is_usuario:
        notificacion = Notificacion.objects.filter(usuario=request.user,tipo="representante")

    return render(request,'notificaciones/listar_notificaciones.html',{'object_list':notificacion})


def UpdateNotificacion(id):
    notificacion = Notificacion.objects.filter(id=id).update(estatus=True)
    return True


class UpdateNotificaciones(LoginRequiredMixin,TemplateView):
    def post(self,request):
        tipo = request.POST['tipo']
        ida = int(request.POST['ida'])
        if ida != 0:
            print('entro aqui')
            notificacion = Notificacion.objects.filter(usuario=ida,tipo=tipo).update(estatus=True)
        else:
            notificacion = Notificacion.objects.filter(tipo=tipo).update(estatus=True)
        return JsonResponse({"success":"Actualizado con exito"},safe=False)





class verusuario(TemplateView):
    model = Users
    template_name = 'administrador/usuario_detail.html'
    def get(self,request,pk):
        if request.GET:
            UpdateNotificacion(int(request.GET['noti']))
        usuario = Users.objects.get(pk=pk)
        return render(request,self.template_name,{'object':usuario,'usuario':usuario})



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Su contrasena fue cambiada exitosamente!')
            return redirect('/login/')
        else:
            messages.error(request, 'Por favor corrija el error.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'administrador/change_password.html', {
        'form': form
    })


