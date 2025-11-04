from datetime import datetime
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db import models
from django.http import Http404
from common.LoggerApp import log_info
from clubs.models.Club import Club
from clubs.models.Season import Season
from clubs.models.ClubCategorie import ClubCategorie
from clubs.models.Register import Register


class HomeTempView(LoginRequiredMixin, TemplateView):
    template_name = "presentations/presentation-club.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        club = Club.get_by_user(user)
        if not club:
            raise Http404("Club no encontrado")
        
        # Clean club name (remove MASTER and FEMENINO)
        club_display_name = club.name.replace('MASTER', '').replace('FEMENINO', '').strip()
        context['club'] = club
        context['club_display_name'] = club_display_name
        
        # Get all club categories with related data
        club_categories = ClubCategorie.objects.filter(club=club).select_related('categorie')
        
        # Get all seasons (ordenadas por fecha de inicio descendente)
        seasons = Season.objects.all().order_by('-start_date')
        
        # Prepare season data with categories and player counts
        prepared_seasons = []
        for season in seasons:
            # Prepare categories data for this season
            category_data = []
            for cc in club_categories:
                # Only show categories that match the season's category
                if season.categorie_id == cc.categorie_id:
                    # Get approved registrations for this season, club and category
                    player_count = Register.objects.filter(
                        season=season,
                        club=club,
                        status='APROBADO'
                    ).count()
                    
                    # Calculate available slots
                    max_players = cc.categorie.max_players
                    if max_players is not None:
                        available_slots = max(0, max_players - player_count)
                        is_full = available_slots <= 0
                    else:
                        available_slots = None
                        is_full = False
                    
                    # Clean category name (remove MASTER and FEMENINO)
                    clean_name = cc.categorie.name.replace('MASTER', '').replace('FEMENINO', '').strip()
                    
                    category_data.append({
                        'id': cc.categorie.id,
                        'name': clean_name,
                        'age_range': f"{cc.categorie.min_age}+ años" if cc.categorie.min_age else "Todas las edades",
                        'max_players': max_players,
                        'description': cc.categorie.description,
                        'registered_players': player_count,
                        'available_slots': available_slots,
                        'is_full': is_full
                    })
            
            # Only add seasons that have matching categories
            if category_data:
                prepared_seasons.append({
                    'id': season.id,
                    'name': season.name,
                    'start_date': season.start_date,
                    'end_date': season.end_date,
                    'categories': category_data
                })
        
        context['seasons'] = prepared_seasons
        
        # Calculate club statistics - sum players from all categories in their most recent seasons
        total_players = 0
        categories_counted = set()
        
        for season in prepared_seasons:
            for category in season['categories']:
                # Only count each category once (from its most recent season)
                if category['id'] not in categories_counted:
                    total_players += category['registered_players']
                    categories_counted.add(category['id'])
        
        context['total_players'] = total_players
        context['total_categories'] = club_categories.count()
        
        log_info(
            user=user,
            url=self.request.path,
            file_name='HomeTempView.py',
            message=f"Usuario accedió a la página de inicio del club {club.name if club else 'Sin club'}"
        )
        
        return context