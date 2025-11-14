from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from clubs.models.Register import Register
from datetime import date


class CarnetReport(TemplateView):
    template_name = "reports/carnet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        registro_id = self.kwargs.get('pk')
        registro = get_object_or_404(Register, pk=registro_id)

        # Validar que el registro tenga temporada y categoría
        if not registro.season or not registro.season.categorie:
            raise ValueError("El registro no tiene una temporada o categoría válida")

        edad = None
        if registro.player.birth_date:
            today = date.today()
            edad = today.year - registro.player.birth_date.year
            if today.month < registro.player.birth_date.month or (
                today.month == registro.player.birth_date.month
                and today.day < registro.player.birth_date.day
            ):
                edad -= 1

        foto_url = registro.photo.url if registro.photo else ""
        logo_url = (
            registro.club.logo.url
            if hasattr(registro.club, "logo") and registro.club.logo
            else ""
        )

        context["registro"] = registro
        context["edad"] = edad
        context["foto_url"] = foto_url
        context["logo_url"] = logo_url
        context["categoria"] = registro.season.categorie.name
        context["numero_jugador"] = registro.number
        context["nombres"] = registro.player.first_name
        context["apellidos"] = registro.player.last_name
        context["cedula"] = registro.player.national_id
        context["club_nombre"] = registro.club.display_name

        return context
