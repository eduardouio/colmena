from django.views.generic import TemplateView

class AllCarnetsReport(TemplateView):
    template_name = "reports/carnet_masivo.html"