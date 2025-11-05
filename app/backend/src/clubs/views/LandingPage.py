from django.views.generic import TemplateView
from django.db.models import Count, Q
from clubs.models.Club import Club
from clubs.models.Register import Register
from clubs.models.Season import Season


class LandingPageView(TemplateView):
    """Vista para mostrar la landing page con información de clubs y jugadores."""
    template_name = "pages/landing.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener clubs activos
        clubs = Club.objects.all().order_by('name')
        
        # Estadísticas generales
        total_clubs = clubs.count()
        total_players = Register.objects.filter(status='APROBADO').values('player').distinct().count()
        total_registers = Register.objects.filter(status='APROBADO').count()
        
        # Temporadas activas
        active_seasons = Season.objects.filter(is_active=True).count()
        
        # Preparar datos de clubs con sus jugadores
        clubs_data = []
        for club in clubs[:6]:  # Mostrar solo los primeros 6 clubs
            approved_players = Register.objects.filter(
                club=club,
                status='APROBADO'
            ).values('player').distinct().count()
            
            # Verificar si el atributo logo existe
            logo_url = None
            if hasattr(club, 'logo') and club.logo:
                logo_url = club.logo.url
            
            club_info = {
                'id': club.id,
                'name': club.name.replace('MASTER', '').replace('FEMENINO', '').strip(),
                'players_count': approved_players,
                'logo': logo_url,
            }
            clubs_data.append(club_info)
        
        context.update({
            'total_clubs': total_clubs,
            'total_players': total_players,
            'total_registers': total_registers,
            'active_seasons': active_seasons,
            'clubs_data': clubs_data,
        })
        
        return context
