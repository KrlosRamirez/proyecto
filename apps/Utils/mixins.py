from django.contrib.auth.mixins import AccessMixin




class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super(AdminRequiredMixin, self).dispatch(request, *args, **kwargs)


class DirectorRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_director:
            return self.handle_no_permission()
        return super(DirectorRequiredMixin, self).dispatch(request, *args, **kwargs)


class SecretariaRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_secretaria:
            return self.handle_no_permission()
        return super(SecretariaRequiredMixin, self).dispatch(request, *args, **kwargs)


class UsuarioRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_usuario:
            return self.handle_no_permission()
        return super(UsuarioRequiredMixin, self).dispatch(request, *args, **kwargs)


class DocenteRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_docente:
            return self.handle_no_permission()
        return super(DocenteRequiredMixin, self).dispatch(request, *args, **kwargs)
