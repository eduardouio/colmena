from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from clubs.models.Club import Club
from clubs.forms.ClubForm import ClubForm
from common.LoggerApp import log_info, log_warning, log_error


class UpdtClubView(LoginRequiredMixin, UpdateView):
    """Vista para actualizar la información del Club"""
    model = Club
    form_class = ClubForm
    template_name = 'forms/club-form.html'
    login_url = 'accounts:login'

    def get_object(self, queryset=None):
        """Obtiene el club asociado al usuario actual"""
        club = Club.get_by_user(self.request.user)
        if club is None:
            raise PermissionError("El usuario no tiene un club asociado")
        return club

    def get_success_url(self):
        """Redirige a la página de presentación del club después de guardar"""
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        """Agrega contexto adicional al template"""
        log_info(
            user=self.request.user,
            url=self.request.path,
            file_name="UpdtClubView",
            message=(
                f"Acceso a formulario de edición de club "
                f"por: {self.request.user.email}"
            ),
            request=self.request
        )
        
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Club"
        context['subtitle'] = "Actualiza la información de tu club"
        return context

    def form_valid(self, form):
        """Maneja el envío exitoso del formulario"""
        club = form.save(commit=False)
        
        # Aquí puedes agregar lógica adicional si es necesaria
        log_info(
            user=self.request.user,
            url=self.request.path,
            file_name="UpdtClubView",
            message=(
                f"Información del club '{club.name}' actualizada "
                f"por: {self.request.user.email}"
            ),
            request=self.request
        )
        
        club.save()
        
        messages.success(
            self.request,
            f"✓ Información del club '{club.name}' actualizada correctamente."
        )
        
        return super().form_valid(form)

    def form_invalid(self, form):
        """Maneja errores en el formulario"""
        log_warning(
            user=self.request.user,
            url=self.request.path,
            file_name="UpdtClubView",
            message=(
                f"Errores de validación en formulario de edición de club "
                f"por: {self.request.user.email}. Errores: {form.errors}"
            ),
            request=self.request
        )
        
        messages.error(
            self.request,
            "✗ Por favor corrige los errores en el formulario."
        )
        
        return super().form_invalid(form)
