from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from clubs.models.Club import Club
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

        # Obtener todas las temporadas con sus registros de jugadores
        seasons_data = []
        seasons = Season.objects.filter(is_active=True).order_by('start_date')
        for season in seasons:
            registers = Register.objects.filter(season=season, club=club).select_related('player')
            
            # Agrupar registros por categoría
            categorie_data = {}
            for register in registers:
                category_id = register.player.category.id if register.player.category else None
                if category_id not in categorie_data:
                    categorie_data[category_id] = {
                        'id': category_id,
                        'name': register.player.category.name if register.player.category else 'Sin categoría',
                        'max_players': register.player.category.max_players if register.player.category else 0,
                        'min_age': register.player.category.min_age if register.player.category else 0,
                        'max_youth_player': register.player.category.max_youth_player if register.player.category else 0,
                        'min_number_player': register.player.category.min_number_player if register.player.category else 0,
                        'max_number_player': register.player.category.max_number_player if register.player.category else 0,
                        'players': [],
                    }
                
                # Agregar datos del jugador
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
                    'photo': register.photo.url if register.photo else None,  # ← AGREGAR ESTA LÍNEA
                }
                categorie_data[category_id]['players'].append(player_data)
            
            # Convertir datos de categoría a lista
            categories_list = list(categorie_data.values())
            
            seasons_data.append({
                'season': season,
                'total_players': registers.count(),
                'categories': categories_list,
            })

        context = {
            'club': club,
            'seasons_data': seasons_data,
            'total_players': sum(data['total_players'] for data in seasons_data),
            'total_seasons': seasons.count(),
        }

        return render(request, 'lists/players_list.html', context)