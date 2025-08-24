from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

from common.BaseModel import BaseModel
from players.models.PlayerModel import Player
from clubs.models.ClubModel import Club
from seasons.models.SeasonModel import Season


class Register(BaseModel):
    """Calificación inicial del aspirante previa a crear el jugador."""

    CATEGORY_CHOICES = [
        ('NIÑOS', 'NIÑOS'),
        ('FEMENINO', 'FEMENINO'),
        ('SENIOR', 'SENIOR'),
        ('MASTER', 'MASTER'),
    ]

    STATUS_CHOICES = [
        ('PENDIENTE', 'PENDIENTE'),
        ('APROBADO', 'APROBADO'),
        ('RECHAZADO', 'RECHAZADO'),
    ]

    season = models.ForeignKey(
        Season, on_delete=models.PROTECT, related_name='registers'
    )
    club = models.ForeignKey(
        Club, on_delete=models.PROTECT
    )
    category = models.CharField(
        'categoría', max_length=10, choices=CATEGORY_CHOICES
    )
    player = models.ForeignKey(
        Player, on_delete=models.PROTECT, related_name='registers'
    )
    number = models.PositiveIntegerField(
        'número jugador'
    )
    minor_authorization = models.FileField(
        'autorización menor', upload_to='autorizaciones/',
        null=True, blank=True
    )
    photo = models.FileField(
        'foto fondo claro',
        upload_to='fotos_registro/',
        blank=True,
        null=True
    )
    id_document = models.FileField(
        'foto cédula',
        upload_to='cedulas/',
        blank=True,
        null=True
    )
    is_requalification = models.BooleanField(
        'recalificación',
        default=False
    )
    status = models.CharField(
        'estado', max_length=10, choices=STATUS_CHOICES, default='PENDIENTE'
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
        unique_together = ['season', 'club', 'category', 'player']
        indexes = [
            models.Index(fields=['season', 'club', 'category']),
            models.Index(fields=['player']),
        ]

    def __str__(self):  # pragma: no cover
        return f"Register {self.pk} - {self.player.full_name if hasattr(self.player, 'full_name') else self.player_id}"

