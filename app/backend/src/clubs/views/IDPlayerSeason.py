from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from clubs.models.Register import Register
from clubs.models.Club import Club


@login_required
def player_id_card(request, register_id):
    """Vista para generar el carnet del jugador."""
    # Obtener el registro
    register = get_object_or_404(
        Register.objects.select_related(
            'player', 
            'club', 
            'season',
            'season__categorie'
        ),
        id=register_id
    )
    
    # Verificar permisos (opcional)
    user_club = Club.get_by_user(request.user)
    if user_club and user_club != register.club and not request.user.is_staff:
        # Puedes añadir restricciones de acceso aquí si lo deseas
        pass
    
    # Calcular edad del jugador
    edad = None
    if register.player.birth_date:
        today = date.today()
        edad = today.year - register.player.birth_date.year
        if today.month < register.player.birth_date.month or \
           (today.month == register.player.birth_date.month and today.day < register.player.birth_date.day):
            edad -= 1
    
    # Limpiar nombre del club (quitar FEMENINO y MASTER)
    club_name = register.club.name
    club_name = club_name.replace('FEMENINO', '').replace('MASTER', '').strip()
    # Limpiar espacios dobles que puedan quedar
    club_name = ' '.join(club_name.split())
    
    # Preparar contexto adaptado al template del carnet
    context = {
        'registro': {
            'numero_jugador': register.number,
            'nombres': register.player.first_name,
            'apellidos': register.player.last_name,
            'cedula': register.player.national_id,
            'categoria': register.season.categorie.name,
            'club': {
                'nombre': club_name  # Usar nombre limpio
            }
        },
        'edad': edad if edad else 'N/A',
        'foto_url': register.photo.url if register.photo else '/static/img/default-player.png',
        'logo_url': '/static/img/logo-colmena.png',  # Logo de la liga
        'temporada': register.season.name,
        'season_year': f"{register.season.start_date.year}-{register.season.end_date.year}" if register.season.start_date and register.season.end_date else "2025-2026"
    }
    
    return render(request, 'presentations/id-player-season.html', context)
