from django.views.generic import TemplateView
from ..models import CalificacionAspirante
from django.utils import timezone
from django.templatetags.static import static
from django.conf import settings
from django.core.paginator import Paginator


class VistaMasivaCarnet(TemplateView):
    template_name = 'registro/carnet-masivo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener el host base dinámicamente desde el request actual
        request = self.request
        protocol = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        base_url = f"{protocol}://{host}"

        # URLs para las imágenes usando el host correcto
        # Logo de la liga
        logo_path = static('img/logo.jpg')
        context['logo_url'] = f"http://146.190.56.181:8000/{logo_path}"

        return context

    def get(self, request, pk=None, *args, **kwargs):
        context = self.get_context_data()

        # Si se proporciona un pk específico, mostrar ese registro individual
        if pk is not None:
            try:
                registro = CalificacionAspirante.objects.get(pk=pk)

                # Calcular la edad
                hoy = timezone.now().date()
                edad = hoy.year - registro.fecha_nacimiento.year - \
                    ((hoy.month, hoy.day) <
                     (registro.fecha_nacimiento.month, registro.fecha_nacimiento.day))

                context['edad'] = edad
                context['registro'] = registro

                # Obtener URL de la foto
                if registro.foto_fondo_claro:
                    context['foto_url'] = f"http://146.190.56.181:8000/{registro.foto_fondo_claro.url}"
                else:
                    default_photo = static('img/perfil-default.png')
                    protocol = 'https' if request.is_secure() else 'http'
                    host = request.get_host()
                    base_url = f"{protocol}://{host}"
                    context['foto_url'] = f"{base_url}{default_photo}"

                return self.render_to_response(context)
            except CalificacionAspirante.DoesNotExist:
                return self.render_to_response({'error': 'Jugador no encontrado'})
        else:
            # Mostrar múltiples registros paginados
            page_number = request.GET.get('page', 1)
            try:
                page_number = int(page_number)
            except ValueError:
                page_number = 1

            # Obtener todos los registros ordenados
            registros = CalificacionAspirante.objects.all().order_by('categoria', 'apellidos')

            # Paginar los resultados (50 por página)
            paginator = Paginator(registros, 50)
            try:
                registros_pagina = paginator.page(page_number)
            except:
                registros_pagina = paginator.page(1)

            # Procesar cada registro para agregar datos necesarios
            registros_procesados = []
            for registro in registros_pagina:
                # Calcular la edad
                hoy = timezone.now().date()
                edad = hoy.year - registro.fecha_nacimiento.year - \
                    ((hoy.month, hoy.day) <
                     (registro.fecha_nacimiento.month, registro.fecha_nacimiento.day))

                # Configurar URL de la foto
                if registro.foto_fondo_claro:
                    foto_url = f"http://146.190.56.181:8000/{registro.foto_fondo_claro.url}"
                else:
                    default_photo = static('img/perfil-default.png')
                    protocol = 'https' if request.is_secure() else 'http'
                    host = request.get_host()
                    base_url = f"{protocol}://{host}"
                    foto_url = f"{base_url}{default_photo}"

                registros_procesados.append({
                    'registro': registro,
                    'edad': edad,
                    'foto_url': foto_url
                })

            context['registros_procesados'] = registros_procesados
            context['page_obj'] = registros_pagina
            context['paginator'] = paginator

            return self.render_to_response(context)
