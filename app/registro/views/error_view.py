from django.views.generic import TemplateView


class ErrorView(TemplateView):
    template_name = 'registro/error.html'
