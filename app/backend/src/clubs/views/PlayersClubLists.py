from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Count, Q, Prefetch
from clubs.models.Club import Club
from clubs.models.Season import Season
from clubs.models.Player import Player
from clubs.models.ClubCategorie import ClubCategorie


class PlayersClubListView(LoginRequiredMixin, ListView):
    """
    Vista para mostrar todos los jugadores de un club organizados por temporada y categoría
    """
    template_name = 'lists/players_list.html'
    context_object_name = 'seasons_data'
    
    def get_queryset(self):
        """
        Obtiene las temporadas con sus categorías y jugadores para el club específico
        """
        club_id = self.kwargs.get('club_id')
        self.club = get_object_or_404(Club, pk=club_id)
        
        # Obtener todas las temporadas relacionadas con el club a través de las categorías
        club_categories = ClubCategorie.objects.filter(
            club=self.club
        ).select_related('categorie')
        
        # Obtener las temporadas que tienen estas categorías
        seasons = Season.objects.filter(
            categorie__in=[cc.categorie for cc in club_categories]
        ).select_related('categorie').order_by('-start_date')
        
        # Organizar los datos por temporada y categoría
        seasons_data = []
        for season in seasons:
            # Aquí deberías obtener los jugadores de cada temporada/categoría
            # Asumiendo que existe una relación entre Player y Season/Categorie
            # Por ahora, devolvemos la estructura básica
            season_data = {
                'season': season,
                'categorie': season.categorie,
                'players': Player.objects.filter(
                    # Aquí filtrarías por los jugadores de esta temporada/categoría
                    # Esto depende de tu modelo de relaciones
                ).order_by('last_name', 'first_name'),
                'total_players': 0  # Actualizar con el conteo real
            }
            # Para propósitos de demostración, obtenemos algunos jugadores
            season_data['players'] = Player.objects.all()[:10]  # Limitar para demo
            season_data['total_players'] = season_data['players'].count()
            seasons_data.append(season_data)
        
        return seasons_data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.club
        
        # Estadísticas generales
        context['total_seasons'] = len(self.get_queryset())
        context['total_players'] = Player.objects.filter(
            # Filtrar por jugadores del club
        ).count()
        
        # Obtener categorías del club
        context['club_categories'] = ClubCategorie.objects.filter(
            club=self.club
        ).select_related('categorie')
        
        return context
