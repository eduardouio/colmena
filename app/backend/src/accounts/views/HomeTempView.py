from datetime import datetime
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from common.LoggerApp import log_info
from clubs.models.Club import Club
from clubs.models.Season import Season
from clubs.models.ClubCategorie import ClubCategorie


class HomeTempView(LoginRequiredMixin, TemplateView):
    template_name = "presentations/presentation-club.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        club = Club.objects.filter(users=user).first()
        context['club'] = club
        
        club_categories = ClubCategorie.objects.filter(club=club).select_related('categorie')
        categories = [cc.categorie for cc in club_categories]
        
        for category in categories:
            category.age_range = f"{category.min_age}+ años" if category.min_age else "Todas las edades"
        
        context['categories'] = categories
        
        championships = Season.objects.filter(
            categorie__in=categories,
            end_date__gte=datetime.now().date()
        ).select_related('categorie')
        
        for championship in championships:
            championship.team_count = 0
        
        context['championships'] = championships
        
        log_info(
            user=user,
            url=self.request.path,
            file_name='HomeTempView.py',
            message=f"Usuario accedió a la página de inicio del club {club.name if club else 'Sin club'}"
        )
        
        return context