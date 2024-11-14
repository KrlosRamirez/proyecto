from django.forms.widgets import TextInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from ..Utils.forms_date import DateInput

class UsersModelForm(UserCreationForm):

    class Meta:
        model = Users
        exclude = ('foto','created_at', 'updated_at', 'groups', 'user_permissions',
            'last_login', 'is_active', 'date_joined', 'password')


class UsersUpdateModelForm(UserChangeForm):
    class Meta:
        model = Users
        exclude = ('foto','created_at', 'updated_at', 'groups', 'user_permissions',
            'last_login', 'is_active', 'date_joined')

class UserCreationForm(UserCreationForm):
	class Meta:
		model = Users
		exclude = ('foto','created_at', 'updated_at', 'groups', 'user_permissions',
            'last_login', 'is_active', 'date_joined')
