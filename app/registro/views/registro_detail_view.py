from django.views.generic import DetailView
from ..models import CalificacionAspirante
from django.templatetags.static import static
from datetime import date


class RegistroDetailView(DetailView):
    model = CalificacionAspirante
    template_name = 'registro/ver-registro.html'
    context_object_name = 'registro'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registro = self.object
        request = self.request

        # Calcular URLs absolutas y edad
        foto_cedula_url = request.build_absolute_uri(registro.foto_cedula.url) if registro.foto_cedula else None
        foto_fondo_claro_url = request.build_absolute_uri(registro.foto_fondo_claro.url) if registro.foto_fondo_claro else None
        logo_url = request.build_absolute_uri(static('img/logo.jpg'))
        logo_colmena = request.build_absolute_uri(static('img/colmena.jpg'))

        today = date.today()
        edad = today.year - registro.fecha_nacimiento.year - ((today.month, today.day) < (registro.fecha_nacimiento.month, registro.fecha_nacimiento.day))

        # Añadir al contexto
        context['foto_cedula_url'] = foto_cedula_url
        context['foto_fondo_claro_url'] = foto_fondo_claro_url
        context['logo_url'] = logo_url
        context['logo_colmena'] = logo_colmena
        context['edad'] = edad

        # Lógica existente para fecha_registro y estado
        if not hasattr(registro, 'fecha_registro'):
            context['registro'].fecha_registro = registro.created_at

        if not hasattr(registro, 'estado'):
            registro.estado = 'pendiente'
            registro.get_estado_display = lambda: 'Pendiente'
            # Asegúrate de que el objeto en el contexto también tenga estos atributos si es necesario
            # context['registro'].estado = 'pendiente' # Ya está en el objeto
            # context['registro'].get_estado_display = lambda: 'Pendiente' # Ya está en el objeto

        return context
