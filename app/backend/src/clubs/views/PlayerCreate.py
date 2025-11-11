from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import datetime, date

from clubs.models.Club import Club
from clubs.models.Player import Player
from clubs.models.Register import Register
from clubs.models.Season import Season
from clubs.models.Categorie import Categorie


class PlayerCreateView(LoginRequiredMixin, View):
    """Vista para crear/registrar un jugador en una temporada."""
    
    def get(self, request, club_id):    
        """Muestra el formulario de registro de jugador."""
        club = get_object_or_404(Club, id=club_id)
        
        # Verificar que el usuario tenga permisos para este club
        if not request.user.is_superuser and club.users != request.user:
            messages.error(request, "No tienes permisos para registrar jugadores en este club.")
            return redirect('home')
        
        # Obtener todas las temporadas activas
        seasons = Season.objects.filter(
            is_active=True
        ).select_related('categorie').order_by('categorie__name', 'name')
        
        context = {
            'club': club,
            'seasons': seasons,
        }
        
        return render(request, 'forms/player_create.html', context)
    
    def validate_category_requirements(self, player, season, number, minor_authorization=None):
        """Valida los requisitos de la categoría antes de crear el registro."""
        category = season.categorie
        errors = []
        
        # Calcular edad del jugador
        player_age = None
        if player.birth_date:
            today = date.today()
            birth_date_obj = player.birth_date if isinstance(player.birth_date, date) else datetime.strptime(player.birth_date, '%Y-%m-%d').date()
            player_age = today.year - birth_date_obj.year
            if today.month < birth_date_obj.month or \
               (today.month == birth_date_obj.month and today.day < birth_date_obj.day):
                player_age -= 1
        
        # Validar edad mínima
        if category.min_age:
            if not player_age:
                errors.append(f'Fecha de nacimiento requerida para validar edad mínima ({category.min_age} años)')
            elif player_age < category.min_age:
                errors.append(f'El jugador debe tener al menos {category.min_age} años para la categoría {category.name}')
        
        # Determinar si es juvenil usando el método de la categoría
        is_youth = category.is_youth_player(player_age)
        
        # Validar rango de números
        if is_youth:
            if number < category.min_number_youth_player or number > category.max_number_youth_player:
                errors.append(f'Jugadores juveniles deben usar números entre {category.min_number_youth_player} y {category.max_number_youth_player}')
            # Solo requerir autorización para menores de 18 años
            if player_age and player_age < 18 and not minor_authorization:
                errors.append('La autorización de menor es obligatoria para jugadores menores de 18 años')
        else:
            if number < category.min_number_player or number > category.max_number_player:
                errors.append(f'Jugadores adultos deben usar números entre {category.min_number_player} y {category.max_number_player}')
        
        return errors, is_youth
    
    def post(self, request, club_id):
        """Procesa el formulario de registro de jugador."""
        club = get_object_or_404(Club, id=club_id)
        
        # Verificar permisos
        if not request.user.is_superuser and club.users != request.user:
            messages.error(request, "No tienes permisos para registrar jugadores en este club.")
            return redirect('home')
        
        try:
            with transaction.atomic():
                # Obtener datos del formulario
                national_id = request.POST.get('national_id', '').strip()
                first_name = request.POST.get('first_name', '').strip()
                last_name = request.POST.get('last_name', '').strip()
                # Usar el email del club en lugar del formulario
                email = club.email if hasattr(club, 'email') and club.email else None
                birth_date_str = request.POST.get('birth_date') or None
                season_id = request.POST.get('season_id')
                number = request.POST.get('number')
                is_requalification = request.POST.get('is_requalification') == 'on'
                have_pass = request.POST.get('have_pass') == 'on'
                before_club = request.POST.get('before_club', '').strip() or None
                
                # Validaciones básicas
                if not all([national_id, first_name, last_name, season_id, number]):
                    raise ValidationError("Por favor complete todos los campos obligatorios.")
                
                # Convertir birth_date de string a objeto date
                birth_date = None
                if birth_date_str:
                    try:
                        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
                    except ValueError:
                        raise ValidationError("Formato de fecha de nacimiento inválido")
                
                # Obtener la temporada
                season = get_object_or_404(Season, id=season_id)
                
                # Convertir number a entero
                try:
                    number = int(number)
                except (ValueError, TypeError):
                    raise ValidationError("El número de jugador debe ser un valor numérico válido")
                
                # Verificar si el jugador ya existe
                player = Player.get_by_national_id(national_id)
                
                if player:
                    # Verificar si ya está registrado en esta temporada con este club
                    existing_register = Register.objects.filter(
                        player=player,
                        club=club,
                        season=season
                    ).first()
                    
                    if existing_register:
                        messages.warning(request, f"El jugador {player.full_name} ya está registrado en esta temporada con este club.")
                        return redirect('clubs:players_list', club_id=club.id)
                    
                    # NUEVA VALIDACIÓN: Verificar si ya está registrado en la misma categoría/temporada en otro club
                    existing_category_register = Register.objects.filter(
                        player=player,
                        season__categorie=season.categorie,
                        season=season,
                        status__in=['PENDIENTE', 'APROBADO']
                    ).exclude(club=club).first()
                    
                    if existing_category_register:
                        messages.error(
                            request, 
                            f"El jugador {player.full_name} ya está registrado en la categoría "
                            f"{season.categorie.name} de la temporada {season.name} "
                            f"con el club {existing_category_register.club.name}. "
                            f"No se puede registrar en la misma categoría y temporada en otro club."
                        )
                        # Mostrar el formulario con los datos para que el usuario vea el error
                        seasons = Season.objects.filter(
                            is_active=True
                        ).select_related('categorie').order_by('categorie__name', 'name')
                        
                        context = {
                            'club': club,
                            'seasons': seasons,
                            'form_data': request.POST,
                            'error_message': f"Jugador ya registrado en {existing_category_register.club.name}"
                        }
                        
                        return render(request, 'forms/player_create.html', context)
                    
                    # Actualizar información del jugador si es necesario
                    player.first_name = first_name
                    player.last_name = last_name
                    # Actualizar email solo si el jugador no tiene uno o si el del club es diferente
                    if email and (not player.email or player.email != email):
                        player.email = email
                    if birth_date:
                        player.birth_date = birth_date
                    player.save()
                    
                    player_status = "existente actualizado y"
                else:
                    # Crear nuevo jugador con el email del club
                    player = Player.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        national_id=national_id,
                        email=email,
                        birth_date=birth_date,
                        has_transfers=have_pass
                    )
                    player_status = "nuevo creado y"
                
                # Manejar archivos
                photo = request.FILES.get('photo')
                id_document = request.FILES.get('id_document')
                minor_authorization = request.FILES.get('minor_authorization')
                
                # Validar requisitos de categoría
                validation_errors, is_youth = self.validate_category_requirements(
                    player, season, number, minor_authorization
                )
                
                if validation_errors:
                    for error in validation_errors:
                        messages.error(request, error)
                    raise ValidationError("No se cumplen los requisitos de la categoría")
                
                # Verificar límites de jugadores
                total_players = Register.objects.filter(
                    season=season,
                    club=club,
                    status='APROBADO'
                ).count()
                
                if total_players >= season.categorie.max_players:
                    raise ValidationError(
                        f"Se alcanzó el límite máximo de {season.categorie.max_players} jugadores para la categoría {season.categorie.name}"
                    )
                
                # Verificar límite de juveniles si aplica
                if is_youth:
                    youth_count = 0
                    today = date.today()
                    for reg in Register.objects.filter(season=season, club=club, status='APROBADO'):
                        if reg.player.birth_date:
                            birth_date_obj = reg.player.birth_date
                            age = today.year - birth_date_obj.year
                            if today.month < birth_date_obj.month or \
                               (today.month == birth_date_obj.month and today.day < birth_date_obj.day):
                                age -= 1
                            # Usar el método de la categoría para determinar si es juvenil
                            if season.categorie.is_youth_player(age):
                                youth_count += 1
                    
                    if youth_count >= season.categorie.max_youth_player:
                        raise ValidationError(
                            f"Se alcanzó el límite máximo de {season.categorie.max_youth_player} jugadores juveniles"
                        )
                
                # Crear el registro
                register = Register.objects.create(
                    season=season,
                    club=club,
                    player=player,
                    number=number,
                    is_requalification=is_requalification,
                    have_pass=have_pass,
                    before_club=before_club,
                    photo=photo,
                    id_document=id_document,
                    minor_authorization=minor_authorization,
                    status='PENDIENTE'
                )
                
                messages.success(
                    request, 
                    f"Jugador {player_status} registrado exitosamente en la temporada {season.name}"
                )
                
                # Verificar si hay otro jugador para registrar
                if 'save_and_new' in request.POST:
                    return redirect('clubs:player_create', club_id=club.id)
                
                return redirect('clubs:players_list', club_id=club.id)
                
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f"Error al registrar el jugador: {str(e)}")
        
        # Si hay error, volver al formulario con los datos
        seasons = Season.objects.filter(
            is_active=True
        ).select_related('categorie').order_by('categorie__name', 'name')
        
        context = {
            'club': club,
            'seasons': seasons,
            'form_data': request.POST
        }
        
        return render(request, 'forms/player_create.html', context)
