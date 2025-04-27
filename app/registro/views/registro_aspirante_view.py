from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.utils import timezone
from ..models import CalificacionAspirante, Club


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
    # Corregido para usar la ruta correcta
    template_name = 'registro/form-registro.html'
    success_url = reverse_lazy('registro:success')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['club'].queryset = Club.objects.all()
        return form

    def form_valid(self, form):
        # Validar autorización para menores de edad
        fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')
        autorizacion = form.cleaned_data.get('autorizacion_menor')

        if fecha_nacimiento:
            hoy = timezone.now().date()
            edad = hoy.year - fecha_nacimiento.year - \
                ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

            # Si es menor de edad y no ha adjuntado autorización
            if edad < 18 and not autorizacion:
                form.add_error(
                    'autorizacion_menor', 'La autorización es obligatoria para menores de edad.')
                return self.form_invalid(form)

            # Si es mayor de edad y adjuntó autorización, simplemente la ignoramos
            if edad >= 18 and autorizacion:
                form.instance.autorizacion_menor = None

        response = super().form_valid(form)
        # Depuración: imprime el objeto guardado
        print("Registro guardado:", self.object)
        return response

    def get_success_url(self):
        # Redirecciona a la vista de detalle después de un registro exitoso
        return reverse_lazy('registro:success', kwargs={'pk': self.object.pk})
