from django.views.generic import DetailView
from ..models import CalificacionAspirante


class RegistroDetailView(DetailView):
    model = CalificacionAspirante
    template_name = 'registro/ver-registro.html'
    context_object_name = 'registro'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Si no existe el campo fecha_registro en el modelo, usar created_at
        if not hasattr(self.object, 'fecha_registro'):
            context['registro'].fecha_registro = self.object.created_at

        # Si no existe el campo estado en el modelo, establecerlo como pendiente
        if not hasattr(self.object, 'estado'):
            # Añadimos métodos dinámicos para la plantilla
            self.object.estado = 'pendiente'
            self.object.get_estado_display = lambda: 'Pendiente'

        return context
