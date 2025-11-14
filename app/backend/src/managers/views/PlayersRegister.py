from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from datetime import date

from clubs.models.Register import Register
from clubs.models.Categorie import Categorie


class PlayersRegister(TemplateView):
    template_name = "managers/players_registers.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect("admin:login")
        return super().dispatch(request, *args, **kwargs)

    def get_age(self, birth_date):
        if not birth_date:
            return None
        today = date.today()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        registros = (
            Register.objects.filter(status__in=["PENDIENTE", "APROBADO"])
            .select_related("player", "club", "season", "season__categorie")
            .order_by("season__name", "season__categorie__name", "club__name", "number")
        )

        agrupados = {}
        for reg in registros:
            season = reg.season
            categoria = season.categorie
            season_key = season.id
            cat_key = categoria.id
            if season_key not in agrupados:
                agrupados[season_key] = {
                    "season": season,
                    "categorias": {}
                }
            if cat_key not in agrupados[season_key]["categorias"]:
                agrupados[season_key]["categorias"][cat_key] = {
                    "categoria": categoria,
                    "registros": []
                }
            edad = self.get_age(reg.player.birth_date)
            agrupados[season_key]["categorias"][cat_key]["registros"].append({
                "registro": reg,
                "edad": edad,
                "carnet_url": reverse("reports:carnet", kwargs={"pk": reg.pk}),
                "pdf_carnet_url": reverse("reports:pdf_carnet", kwargs={"registro_id": reg.pk}),
            })

        # Transformar a lista para el template
        seasons_list = []
        for sdata in agrupados.values():
            categorias_list = []
            for cdata in sdata["categorias"].values():
                categorias_list.append(cdata)
            seasons_list.append({
                "season": sdata["season"],
                "categorias": categorias_list
            })

        # Botones PDF masivo por categoría (FEMENINO, MASTER, SENIOR)
        categorias_objs = Categorie.objects.filter(name__in=["FEMENINO", "MASTER", "SENIOR"])
        botones = []
        for cat in categorias_objs:
            botones.append({
                "nombre": cat.name.title(),
                "pdf_url": reverse("reports:pdf_carnets_categoria", kwargs={"categoria_id": cat.id})
            })

        context["seasons_data"] = seasons_list
        context["categoria_botones"] = botones
        return context
