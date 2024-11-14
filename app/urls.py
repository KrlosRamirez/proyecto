"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from apps.Usuario.views import *
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('medicamentos/',include(('apps.Medicamentos.urls','medicamentos'))),
    path('usuarios/',include(('apps.Usuario.urls','usuarios'))),
   # path('reportes/',include(('apps.Reportes.urls','reportes'))),
    path('',LoginView.as_view(template_name='comun/login.html'), name='login'),


]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


