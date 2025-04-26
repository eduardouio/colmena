from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .models import CalificacionAspirante, Club

class RegistroAspiranteView(CreateView):
    model = CalificacionAspirante
    fields = [
        'email',
        'temporada',
        'club',
        'categoria',
        'nombres',
        'apellidos',
        'cedula',
        'fecha_nacimiento',
        'numero_jugador',
        'tiene_pases',
        'autorizacion_menor',
        'foto_fondo_claro',
        'foto_cedula',
        'recalificacion',
    ]
    template_name = 'registro/form-registro.html'  # Corregido para usar la ruta correcta
    success_url = reverse_lazy('registro:success')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['club'].queryset = Club.objects.all()
        return form

class SuccessView(TemplateView):
    template_name = 'registro/success.html'

class ErrorView(TemplateView):
    template_name = 'registro/error.html'
