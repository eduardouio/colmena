from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'registro/home_success.html'