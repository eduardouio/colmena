from datetime import date
from django.db import models
from django.utils import timezone
from .Club import Club
from .Player import Player
from .Categorie import Categorie
from common.BaseModel import BaseModel


class Season(BaseModel):
    id = models.AutoField(
        primary_key=True
    )
    name = models.CharField(
        'nombre',
        max_length=120, unique=True
    )
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.PROTECT,
        related_name='seasons'
    )
    start_date = models.DateField(
        'fecha inicio'
    )
    end_date = models.DateField(
        'fecha fin'
    )
    is_active = models.BooleanField(
        'activa',
        default=True,
        help_text='Indica si la temporada está activa'
    )
    winner = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='season_wins'
    )
    second = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='season_second_places'
    )
    third = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='season_third_places'
    )
    scoring_player = models.ForeignKey(
        Player,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='scoring_achievements'
    )

    class Meta:
        unique_together = ('categorie', 'name')
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} - {self.categorie.name}"
