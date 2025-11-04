from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date
from clubs.models.Register import Register
from clubs.models.Club import Club


@login_required
def player_register_presentation(request, register_id):
    """Vista para mostrar la presentación del registro de un jugador."""
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
    
    # Verificar permisos (opcional - ajustar según tu lógica)
    user_club = Club.get_by_user(request.user)
    if user_club and user_club != register.club and not request.user.is_staff:
        # Si el usuario tiene un club asociado y no es el mismo del registro
        # y no es staff, puede que quieras restringir el acceso
        pass
    
    # Calcular edad del jugador
    player_age = None
    is_youth = False
    if register.player.birth_date:
        today = date.today()
        player_age = today.year - register.player.birth_date.year
        if today.month < register.player.birth_date.month or \
           (today.month == register.player.birth_date.month and today.day < register.player.birth_date.day):
            player_age -= 1
        
        # Determinar si es juvenil
        if register.season.categorie.name in ['SENIOR', 'FEMENINO'] and player_age < 18:
            is_youth = True
    
    # Obtener otros registros del jugador (historial)
    player_history = Register.objects.filter(
        player=register.player
    ).select_related(
        'club', 
        'season',
        'season__categorie'
    ).exclude(
        id=register.id
    ).order_by('-season__start_date')[:5]
    
    # Contar totales para estadísticas
    total_seasons = Register.objects.filter(
        player=register.player,
        status='APROBADO'
    ).values('season').distinct().count()
    
    total_clubs = Register.objects.filter(
        player=register.player,
        status='APROBADO'
    ).values('club').distinct().count()
    
    # Verificar documentos
    has_all_documents = all([
        register.photo,
        register.id_document,
        not is_youth or register.minor_authorization  # Si es juvenil, necesita autorización
    ])
    
    context = {
        'register': register,
        'player': register.player,
        'club': register.club,
        'season': register.season,
        'category': register.season.categorie,
        'player_age': player_age,
        'is_youth': is_youth,
        'player_history': player_history,
        'total_seasons': total_seasons,
        'total_clubs': total_clubs,
        'has_all_documents': has_all_documents,
    }
    
    return render(request, 'presentations/presentation-player-register.html', context)
