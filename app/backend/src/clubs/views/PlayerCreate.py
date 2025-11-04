from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import datetime

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
                email = request.POST.get('email', '').strip() or None
                birth_date = request.POST.get('birth_date') or None
                season_id = request.POST.get('season_id')
                number = request.POST.get('number')
                is_requalification = request.POST.get('is_requalification') == 'on'
                have_pass = request.POST.get('have_pass') == 'on'
                before_club = request.POST.get('before_club', '').strip() or None
                
                # Validaciones básicas
                if not all([national_id, first_name, last_name, season_id, number]):
                    raise ValidationError("Por favor complete todos los campos obligatorios.")
                
                # Obtener la temporada
                season = get_object_or_404(Season, id=season_id)
                
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
                        messages.warning(request, f"El jugador {player.full_name} ya está registrado en esta temporada.")
                        return redirect('clubs:players_list', club_id=club.id)
                    
                    # Actualizar información del jugador si es necesario
                    player.first_name = first_name
                    player.last_name = last_name
                    if email:
                        player.email = email
                    if birth_date:
                        player.birth_date = birth_date
                    player.save()
                    
                    player_status = "existente actualizado y"
                else:
                    # Crear nuevo jugador
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
