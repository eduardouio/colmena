from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from common.BaseModel import BaseModel
from .Season import Season
from .Player import Player
from .Club import Club



class Register(BaseModel):
    """Calificación inicial del aspirante previa a crear el jugador."""
    STATUS_CHOICES = [
        ('PENDIENTE', 'PENDIENTE'),
        ('APROBADO', 'APROBADO'),
        ('RECHAZADO', 'RECHAZADO'),
    ]
    season = models.ForeignKey(
        Season, 
        on_delete=models.PROTECT,
        related_name='registers'
    )
    club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        related_name='registers'
    )
    player = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        related_name='registers'
    )
    number = models.PositiveIntegerField(
        'número jugador'
    )
    minor_authorization = models.FileField(
        'autorización menor',
        upload_to='autorizaciones/',
        max_length=255,
        null=True, blank=True
    )
    photo = models.FileField(
        'foto fondo claro',
        upload_to='fotos_registro/',
        max_length=255,
        blank=True,
        null=True
    )
    id_document = models.FileField(
        'foto cédula',
        upload_to='cedulas/',
        max_length=255,
        blank=True,
        null=True
    )
    is_requalification = models.BooleanField(
        'recalificación',
        default=False
    )
    status = models.CharField(
        'estado', 
        max_length=10, choices=STATUS_CHOICES,
        default='PENDIENTE'
    )
    have_pass = models.BooleanField(
        'tiene pase',
        default=False
    )
    before_club = models.CharField(
        'club Anterior', max_length=100, blank=True, null=True
    )

    class Meta:
        verbose_name = 'Registro aspirante'
        verbose_name_plural = 'Registros aspirantes'
        ordering = ['-created_at']
        unique_together = ['club', 'player', 'season']
        

    def __str__(self):
        return f"{self.player.full_name} - {self.club.name} (Temporada: {self.season.name})"
    
    def clean(self):
        """Validación personalizada del registro."""
        super().clean()
        self.validate_no_duplicate_category_season()
        self.validate_category_rules()
        self.validate_unique_number()
    
    def validate_no_duplicate_category_season(self):
        """Valida que el jugador no esté registrado en la misma categoría y temporada en otro club."""
        if not self.player or not self.season or not self.season.categorie:
            return
            
        # Buscar registros existentes del mismo jugador en la misma categoría y temporada
        existing_registers = Register.objects.filter(
            player=self.player,
            season__categorie=self.season.categorie,
            season=self.season,
            status__in=['PENDIENTE', 'APROBADO']
        ).exclude(pk=self.pk)
        
        if existing_registers.exists():
            existing_register = existing_registers.first()
            raise ValidationError(
                f'El jugador {self.player.full_name} ya está registrado en la categoría '
                f'{self.season.categorie.name} de la temporada {self.season.name} '
                f'con el club {existing_register.club.name}. '
                f'No se puede registrar en la misma categoría y temporada en otro club.'
            )

    def validate_category_rules(self):
        """Valida las reglas específicas de la categoría."""
        if not self.season or not self.season.categorie:
            return
            
        category = self.season.categorie
        
        # Calcular edad del jugador si tiene fecha de nacimiento
        player_age = None
        if self.player and self.player.birth_date:
            today = date.today()
            player_age = today.year - self.player.birth_date.year
            if today.month < self.player.birth_date.month or \
               (today.month == self.player.birth_date.month and today.day < self.player.birth_date.day):
                player_age -= 1
        
        # Validar edad mínima
        if category.min_age and player_age and player_age < category.min_age:
            raise ValidationError(f'El jugador debe tener al menos {category.min_age} años para esta categoría')
        
        # Determinar si es juvenil usando el método de la categoría
        is_youth = category.is_youth_player(player_age)
        
        # Validar rango de números según edad
        if is_youth:
            if self.number < category.min_number_youth_player or self.number > category.max_number_youth_player:
                raise ValidationError(
                    f'Los jugadores juveniles deben usar números entre {category.min_number_youth_player} y {category.max_number_youth_player}'
                )
            # Verificar autorización para menores (solo para menores de 18)
            if player_age and player_age < 18 and not self.minor_authorization:
                raise ValidationError('La autorización de menor es obligatoria para jugadores menores de 18 años')
        else:
            if self.number < category.min_number_player or self.number > category.max_number_player:
                raise ValidationError(
                    f'Los jugadores adultos deben usar números entre {category.min_number_player} y {category.max_number_player}'
                )
        
        # Contar jugadores actuales en la categoría
        total_players = Register.objects.filter(
            season=self.season,
            club=self.club,
            status='APROBADO'
        ).exclude(pk=self.pk).count()
        
        if total_players >= category.max_players:
            raise ValidationError(f'Se alcanzó el límite máximo de {category.max_players} jugadores para esta categoría')
        
        # Contar jugadores juveniles si aplica
        if is_youth:
            youth_players = 0
            today = date.today()
            for reg in Register.objects.filter(season=self.season, club=self.club, status='APROBADO').exclude(pk=self.pk):
                if reg.player.birth_date:
                    reg_age = today.year - reg.player.birth_date.year
                    if today.month < reg.player.birth_date.month or \
                       (today.month == reg.player.birth_date.month and today.day < reg.player.birth_date.day):
                        reg_age -= 1
                    if category.is_youth_player(reg_age):
                        youth_players += 1
            
            if youth_players >= category.max_youth_player:
                raise ValidationError(f'Se alcanzó el límite máximo de {category.max_youth_player} jugadores juveniles')
    
    def validate_unique_number(self):
        """Valida que el número sea único en la temporada/club."""
        if self.number and self.season and self.club:
            exists = Register.objects.filter(
                season=self.season,
                club=self.club,
                number=self.number
            ).exclude(pk=self.pk).exists()
            
            if exists:
                raise ValidationError(f'El número {self.number} ya está asignado a otro jugador en esta temporada')
