from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users
import django

from django.utils.translation import gettext_lazy as _


# Registre sus modelos aquí.

class UsersAdmin(UserAdmin):
	list_display = ('username','is_admin','is_usuario','is_staff','date_joined', 'last_login')
	readonly_fields=('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(Users, UsersAdmin)
