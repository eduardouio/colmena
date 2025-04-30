from django.views.generic import TemplateView
from ..models import CalificacionAspirante
from django.utils import timezone
from django.templatetags.static import static


class VistaCarnet(TemplateView):
    template_name = 'registro/carnet.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registro = context['registro']
        
        # Calcular la edad
        hoy = timezone.now().date()
        edad = hoy.year - registro.fecha_nacimiento.year - ((hoy.month, hoy.day) < (registro.fecha_nacimiento.month, registro.fecha_nacimiento.day))
        
        # Agregar datos adicionales al contexto
        context['edad'] = edad
        
        # URLs para las imágenes
        if self.request:
            # Logo de la liga
            context['logo_url'] = self.request.build_absolute_uri(static('img/logo.jpg'))
            
            # Foto del jugador (si existe)
            if registro.foto_fondo_claro:
                context['foto_url'] = self.request.build_absolute_uri(registro.foto_fondo_claro.url)
            else:
                context['foto_url'] = self.request.build_absolute_uri(static('img/perfil-default.png'))
            
            # URL para el QR
            context['qr_url'] = f"https://api.qrserver.com/v1/create-qr-code/?size=60x60&data=https://liga.com/jugador/{registro.pk}"
            
        return context

    def get(self, request, pk, *args, **kwargs):
        try:
            registro = CalificacionAspirante.objects.get(pk=pk)
            context = self.get_context_data(registro=registro)
            return self.render_to_response(context)
        except CalificacionAspirante.DoesNotExist:
            # Manejar el caso donde no exista el registro
            return self.render_to_response({'error': 'Jugador no encontrado'})