from django.views.generic import TemplateView
from registro.models import CalificacionAspirante

class SuccessView(TemplateView):
    template_name = 'registro/success.html'

    def get(self, request, pk, *args, **kwargs):
        registro = CalificacionAspirante.objects.get(pk=pk)
        context = self.get_context_data(registro=registro)
        return self.render_to_response(context)
