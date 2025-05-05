from django.views.generic import TemplateView
from ..models import CalificacionAspirante
from django.utils import timezone
from django.templatetags.static import static
from django.conf import settings


class VistaCarnet(TemplateView):
    template_name = 'registro/carnet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registro = context['registro']

        # Calcular la edad
        hoy = timezone.now().date()
        edad = hoy.year - registro.fecha_nacimiento.year - \
            ((hoy.month, hoy.day) <
             (registro.fecha_nacimiento.month, registro.fecha_nacimiento.day))

        # Agregar datos adicionales al contexto
        context['edad'] = edad

        # Obtener el host base dinámicamente desde el request actual
        request = self.request
        protocol = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        base_url = f"{protocol}://{host}"
        
        # URLs para las imágenes usando el host correcto
        # Logo de la liga
        logo_path = static('img/logo.jpg')
        context['logo_url'] = f"http://146.190.56.181:8000/{logo_path}"

        # Foto del jugador (si existe)
        if registro.foto_fondo_claro:
            context['foto_url'] = f"http://146.190.56.181:8000/{registro.foto_fondo_claro.url}"
        else:
            default_photo = static('img/perfil-default.png')
            context['foto_url'] = f"{base_url}{default_photo}"

        return context

    def get(self, request, pk, *args, **kwargs):
        try:
            registro = CalificacionAspirante.objects.get(pk=pk)
            context = self.get_context_data(registro=registro)
            return self.render_to_response(context)
        except CalificacionAspirante.DoesNotExist:
            # Manejar el caso donde no exista el registro
            return self.render_to_response({'error': 'Jugador no encontrado'})
