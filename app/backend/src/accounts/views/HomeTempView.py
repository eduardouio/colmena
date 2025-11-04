from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from common.LoggerApp import log_info
from clubs.models.Club import Club
from clubs.models.Player import Player
from clubs.models.Season import Season
from clubs.models.ClubCategorie import ClubCategorie
from django.utils import timezone


class HomeTempView(LoginRequiredMixin, TemplateView):
    template_name = "presentations/presentation-club.html"

    def get_context_data(self, **kwargs):
        log_info(
            user=self.request.user,
            url=self.request.path,
            file_name="HomeTempView",
            message=f"Acceso a página principal por: {self.request.user.email}",
            request=self.request
        )
        
        context = super().get_context_data(**kwargs)
        
        # Obtener el club del usuario actual (ajusta según tu lógica de autenticación)
        try:
            club = Club.objects.first()  # Obtener el club correspondiente al usuario
        except Club.DoesNotExist:
            club = None
        
        # Obtener campeonatos activos (fecha actual entre start_date y end_date)
        today = timezone.now().date()
        championships = Season.objects.filter(
            start_date__lte=today,
            end_date__gte=today
        ).order_by('start_date')[:3]  # Limitar a 3 campeonatos
        
        # Obtener jugadores del club (ajusta según tu modelo de relación)
        players = Player.objects.all()[:5]  # Limitar a 5 jugadores
        
        # Obtener categorías del club
        categories = ClubCategorie.objects.filter(club=club).select_related('categorie')[:5]  # Limitar a 5 categorías
        
        # Agregar datos al contexto
        context.update({
            'title': f"Bienvenido a {club.name if club else 'tu club'}",
            'club': club,
            'championships': [{
                'id': champ.id,
                'name': champ.name,
                'start_date': champ.start_date,
                'end_date': champ.end_date,
                'team_count': 8  # Valor de ejemplo, ajusta según tu modelo
            } for champ in championships],
            'categories': [{
                'id': cat.id,
                'name': cat.categorie.name,
                'description': cat.categorie.description or 'Sin descripción',
                'age_range': f"{cat.categorie.min_age} - {cat.categorie.max_age} años"
            } for cat in categories],
            'players': [{
                'id': player.id,
                'first_name': player.first_name,
                'last_name': player.last_name,
                'national_id': player.national_id,
                'age': 25,  # Calcular la edad a partir de la fecha de nacimiento
                'position': 'Delantero'  # Ajusta según tu modelo
            } for player in players]
        })
        
        return context