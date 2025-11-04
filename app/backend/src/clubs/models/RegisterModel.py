from django.db import models
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
        unique_together = ['club_categorie', 'player']
        

    def __str__(self):
        return f"{self.player.full_name} - {self.club_categorie.club.name} ({self.club_categorie.categorie.name})"
