from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
from clubs.models.Register import Register
from clubs.models.Club import Club


class PlayerSheetView(LoginRequiredMixin, View):
    """Vista para generar la ficha imprimible del jugador."""
    
    def get(self, request, register_id):
        register = get_object_or_404(
            Register.objects.select_related(
                'player', 
                'club', 
                'season',
                'season__categorie'
            ),
            id=register_id
        )
        
        user_club = Club.get_by_user(request.user)
        if user_club and user_club != register.club and not request.user.is_staff:
            pass
        
        player_age = None
        is_youth = False
        if register.player.birth_date:
            today = date.today()
            player_age = today.year - register.player.birth_date.year
            if today.month < register.player.birth_date.month or \
               (today.month == register.player.birth_date.month and today.day < register.player.birth_date.day):
                player_age -= 1
            
            if register.season.categorie.name in ['SENIOR', 'FEMENINO'] and player_age < 18:
                is_youth = True
        
        season_start_year = register.season.start_date.year if register.season.start_date else None
        season_end_year = register.season.end_date.year if register.season.end_date else None
        
        club_name = register.club.name
        club_name = club_name.replace('FEMENINO', '').replace('MASTER', '').strip()
        club_name = ' '.join(club_name.split())
        
        context = {
            'register': register,
            'player': register.player,
            'club': register.club,
            'club_display_name': club_name,
            'season': register.season,
            'category': register.season.categorie,
            'player_age': player_age,
            'is_youth': is_youth,
            'season_start_year': season_start_year,
            'season_end_year': season_end_year,
            'qualification_date': register.created_at.date() if register.created_at else None,
            'approval_date': register.updated_at.date() if register.status == 'APROBADO' and register.updated_at else None,
        }
        
        if request.GET.get('print') == 'true':
            response = render(request, 'presentations/player-sheet.html', context)
            response['Content-Type'] = 'text/html; charset=utf-8'
            return response
        
        return render(request, 'presentations/player-sheet.html', context)
