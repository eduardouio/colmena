from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from datetime import date
from clubs.models.Club import Club
from clubs.models.Season import Season
from clubs.models.ClubCategorie import ClubCategorie
from clubs.models.Register import Register


class PlayersClubListView(LoginRequiredMixin, ListView):
    """
    Vista para mostrar todos los jugadores de un club organizados por temporada y categoría
    """
    template_name = 'lists/players_list.html'
    context_object_name = 'seasons_data'
    
    def calculate_age(self, birth_date):
        """
        Calcula la edad basándose en la fecha de nacimiento
        """
        if not birth_date:
            return None
        
        today = date.today()
        age = today.year - birth_date.year
        
        # Ajustar si aún no ha cumplido años este año
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        
        return age
    
    def get_queryset(self):
        """
        Obtiene las temporadas con sus categorías y jugadores para el club específico
        """
        club_id = self.kwargs.get('club_id')
        self.club = get_object_or_404(Club, pk=club_id)
        
        # Obtener las categorías registradas del club
        club_categories = ClubCategorie.objects.filter(
            club=self.club
        ).select_related('categorie')
        
        # Extraer solo los IDs de las categorías
        categories_ids = [cc.categorie.id for cc in club_categories]
        
        # Obtener SOLO las temporadas de las categorías que el club tiene registradas
        seasons = Season.objects.filter(
            categorie_id__in=categories_ids
        ).select_related('categorie').order_by('-start_date')
        
        # Organizar los datos por temporada y categoría
        seasons_data = []
        for season in seasons:
            # Verificar que esta categoría esté registrada en el club
            club_categorie = club_categories.filter(
                categorie=season.categorie
            ).first()
            
            if club_categorie:
                # Obtener los registros (jugadores inscritos) para esta temporada y club
                registers = Register.objects.filter(
                    season=season,
                    club=self.club
                ).select_related('player').order_by('player__last_name', 'player__first_name')
                
                # Solo agregar la temporada si tiene jugadores registrados
                if registers.exists():
                    # Crear lista de jugadores con información adicional del registro
                    players_data = []
                    for register in registers:
                        player = register.player
                        # Añadir información del registro al jugador
                        player.register_id = register.id  # Agregar el ID del registro
                        player.jersey_number = register.number
                        player.registration_status = register.status
                        player.is_requalification = register.is_requalification
                        player.registration_date = register.created_at  # Fecha de registro
                        player.register_photo = register.photo  # Foto del registro
                        # Calcular y añadir la edad
                        player.age = self.calculate_age(player.birth_date)
                        players_data.append(player)
                    
                    season_data = {
                        'season': season,
                        'categorie': season.categorie,
                        'club_categorie': club_categorie,
                        'players': players_data,
                        'total_players': len(players_data)
                    }
                    
                    seasons_data.append(season_data)
        
        return seasons_data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['club'] = self.club
        
        # Estadísticas generales
        seasons_data = self.get_queryset()
        context['total_seasons'] = len(seasons_data)
        
        # Total de jugadores únicos registrados en el club (en todas las temporadas)
        context['total_players'] = Register.objects.filter(
            club=self.club
        ).values('player').distinct().count()
        
        # Obtener categorías del club
        context['club_categories'] = ClubCategorie.objects.filter(
            club=self.club
        ).select_related('categorie')
        
        return context
