from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from clubs.models.Club import Club
from clubs.models.ClubCategorie import ClubCategorie
from clubs.models.Register import Register
from clubs.models.Season import Season


class PlayersListView(LoginRequiredMixin, View):
    """Vista para listar jugadores de un club en una temporada."""

    def get(self, request, club_id):
        """Muestra la lista de jugadores por temporada y categoría."""
        club = get_object_or_404(Club, id=club_id)

        # Verificar que el usuario tenga permisos para este club
        if not request.user.is_superuser and club.users != request.user:
            return render(request, '403.html', status=403)

        # Obtener categorías del club
        club_categories = ClubCategorie.objects.filter(club=club).select_related('categorie')

        # Obtener todas las temporadas con sus registros de jugadores
        seasons_data = []
        seasons = Season.objects.filter(is_active=True).order_by('-start_date')
        
        for season in seasons:
            # Obtener registros para esta temporada y club
            registers = Register.objects.filter(
                season=season, 
                club=club
            ).select_related('player').order_by('number')
            
            if registers.exists():
                # Tomar la categoría de la temporada
                categorie = season.categorie
                
                # Construir lista de jugadores con todos sus datos
                players = []
                for register in registers:
                    player_data = {
                        'full_name': register.player.full_name,
                        'first_name': register.player.first_name,
                        'last_name': register.player.last_name,
                        'national_id': register.player.national_id,
                        'birth_date': register.player.birth_date,
                        'age': register.player.age if hasattr(register.player, 'age') else None,
                        'jersey_number': register.number,
                        'registration_date': register.created_at,
                        'registration_status': register.status,
                        'is_requalification': register.is_requalification,
                        'has_transfers': register.player.has_transfers,
                        'photo': register.photo.url if register.photo else None,
                    }
                    players.append(player_data)
                
                season_data = {
                    'season': season,
                    'categorie': categorie,
                    'total_players': len(players),
                    'players': players,
                }
                seasons_data.append(season_data)

        context = {
            'club': club,
            'club_categories': club_categories,
            'seasons_data': seasons_data,
            'total_players': sum(data['total_players'] for data in seasons_data),
            'total_seasons': len(seasons_data),
        }

        return render(request, 'lists/players_list.html', context)