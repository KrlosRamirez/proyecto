from ..Usuario.models import Notificacion

def notificacion(request):
	if request.user.is_authenticated:
		if request.user.is_superuser:
			notificacion = Notificacion.objects.filter(tipo="superuser").order_by('-id')[:5]
			pendientes = Notificacion.objects.filter(tipo="superuser",estatus=False).order_by('-id')[:5]
			pen = len(pendientes)

		if request.user.is_admin:
			notificacion = Notificacion.objects.filter(tipo="administrador").order_by('-id')[:5]
			pendientes = Notificacion.objects.filter(tipo="administrador",estatus=False).order_by('-id')[:5]
			pen = len(pendientes)
		
		if request.user.is_usuario:
			notificacion = Notificacion.objects.filter(usuario=request.user,tipo="jefe_familia").order_by('-id')[:5]
			pendientes = Notificacion.objects.filter(usuario=request.user,tipo="jefe_familia",estatus=False).order_by('-id')[:5]
			pen = len(pendientes)

		
	else:
		notificacion = ''
		pen = ''
	return {'notificaciones':notificacion,'pendientes':pen}