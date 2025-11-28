from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from clubs.models.Register import Register
from clubs.models.Categorie import Categorie
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date


class AllCarnetsReport(TemplateView):
    template_name = "reports/carnet_masivo.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        categoria_id = self.kwargs.get('categoria_id')
        categoria = get_object_or_404(Categorie, pk=categoria_id)
        
        # Obtener todos los registros aprobados de la categoría
        registros = Register.objects.filter(
            season__categorie=categoria,
            status='APROBADO'
        ).select_related('player', 'club', 'season')
        
        # Preparar los datos de cada registro
        carnets_data = []
        for registro in registros:
            edad = None
            if registro.player.birth_date:
                today = date.today()
                edad = today.year - registro.player.birth_date.year
                if today.month < registro.player.birth_date.month or (
                    today.month == registro.player.birth_date.month
                    and today.day < registro.player.birth_date.day
                ):
                    edad -= 1
            
            foto_url = registro.photo.url if registro.photo else ""
            
            carnets_data.append({
                'registro': registro,
                'edad': edad,
                'foto_url': foto_url,
                'categoria': categoria.name
            })
        
        context['carnets'] = carnets_data
        context['categoria'] = categoria.name
        context['total_carnets'] = len(carnets_data)
        
        return context
    
