from django.db import models
from common.BaseModel import BaseModel

CATEGORIES = (
    ('FEMENINO', 'FEMENINO'),
    ('MASTER', 'MASTER'),
    ('SENIOR', 'SENIOR'),
)

class Categorie(BaseModel):
    """
    Modelo para las categorías de los clubes.
    
    Las categorías pueden ser: FEMENINO, MASTER, SENIOR, etc.
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name='ID'
    )
    name = models.CharField(
        'categoría',
        max_length=20,
        choices=CATEGORIES,
        default='FEMENINO'
    )    
    description = models.TextField(
        'descripción',
        blank=True,
        null=True,
        help_text='Descripción detallada de la categoría'
    )
    
    min_age = models.PositiveIntegerField(
        'edad mínima',
        null=True,
        blank=True,
        help_text='Edad mínima para esta categoría (opcional)'
    )
    max_players = models.PositiveIntegerField(
        'maximo de jugadores',
        default=20,
        help_text='Maximo de jugadores para esta categoría'
    )
    max_youth_player = models.PositiveIntegerField(
        'maximo juvenil',
        default=20,
        help_text='Maximo de jugadores juveniles para esta categoría'
    )
    min_number_youth_player = models.PositiveIntegerField(
        'Numero Minimo Juvenil',
        default=12,
        help_text='minimo numero de camisena juvenil'
    )
    max_number_youth_player = models.PositiveIntegerField(
        'Numero Maximo Juvenil',
        default=12,
        help_text='maximo numero de camisena juvenil'
    )
    min_number_player = models.PositiveIntegerField(
        'Numero Minimo',
        default=1,
        help_text='minimo numero de camisena'
    )
    max_number_player = models.PositiveIntegerField(
        'Numero Maximo',
        default=49,
        help_text='maximo numero de camisena'
    )    
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
        db_table = 'categories'
    
    def __str__(self):
        return self.name
