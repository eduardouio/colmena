from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from datetime import datetime

from clubs.models.Player import Player
from clubs.models.Register import Register
from clubs.models.Season import Season


@method_decorator(csrf_exempt, name='dispatch')
class CheckPlayerExistView(View):
    """
    Vista API para verificar si un jugador existe por su número de cédula.
    Retorna información del jugador y su club actual si existe.
    """
    
    def get(self, request):
        """
        GET /api/check-player/?national_id=1234567890
        """
        national_id = request.GET.get('national_id', '').strip()
        
        if not national_id:
            return JsonResponse({
                'success': False,
                'error': 'Parámetro national_id es requerido'
            }, status=400)
        
        # Verificar si el jugador existe
        player = Player.get_by_national_id(national_id)
        
        if not player:
            return JsonResponse({
                'success': True,
                'exists': False,
                'message': 'Jugador no encontrado'
            })
        
        # Buscar el registro más reciente del jugador en temporadas activas
        current_register = Register.objects.filter(
            player=player,
            season__is_active=True
        ).select_related('club', 'season', 'season__categorie').first()
        
        response_data = {
            'success': True,
            'exists': True,
            'player': {
                'id': player.id,
                'full_name': player.full_name,
                'first_name': player.first_name,
                'last_name': player.last_name,
                'national_id': player.national_id,
                'email': player.email,
                'birth_date': player.birth_date.isoformat() if player.birth_date else None,
                'has_transfers': player.has_transfers
            }
        }
        
        if current_register:
            response_data['current_registration'] = {
                'club': {
                    'id': current_register.club.id,
                    'name': current_register.club.name
                },
                'season': {
                    'id': current_register.season.id,
                    'name': current_register.season.name,
                    'category': current_register.season.categorie.name
                },
                'number': current_register.number,
                'status': current_register.status,
                'is_requalification': current_register.is_requalification,
                'have_pass': current_register.have_pass,
                'before_club': current_register.before_club
            }
        else:
            # Buscar el último registro histórico
            last_register = Register.objects.filter(
                player=player
            ).select_related('club', 'season', 'season__categorie').order_by('-created_at').first()
            
            if last_register:
                response_data['last_registration'] = {
                    'club': {
                        'id': last_register.club.id,
                        'name': last_register.club.name
                    },
                    'season': {
                        'id': last_register.season.id,
                        'name': last_register.season.name,
                        'category': last_register.season.categorie.name
                    },
                    'status': last_register.status,
                    'registered_at': last_register.created_at.isoformat()
                }
            else:
                response_data['current_registration'] = None
                response_data['message'] = 'Jugador existe pero no tiene registros en ninguna temporada'
        
        return JsonResponse(response_data)
    
    def post(self, request):
        """
        POST /api/check-player/
        Body: {"national_id": "1234567890"}
        """
        import json
        
        try:
            data = json.loads(request.body)
            national_id = data.get('national_id', '').strip()
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'JSON inválido'
            }, status=400)
        
        if not national_id:
            return JsonResponse({
                'success': False,
                'error': 'Campo national_id es requerido'
            }, status=400)
        
        # Reutilizar la lógica del GET
        request.GET = request.GET.copy()
        request.GET['national_id'] = national_id
        return self.get(request)
