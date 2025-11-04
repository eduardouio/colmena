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
    
    # Nuevos campos para definir el rango de edad juvenil
    youth_min_age = models.PositiveIntegerField(
        'edad mínima juvenil',
        null=True,
        blank=True,
        help_text='Edad mínima para ser considerado juvenil en esta categoría'
    )
    youth_max_age = models.PositiveIntegerField(
        'edad máxima juvenil',
        null=True,
        blank=True,
        help_text='Edad máxima para ser considerado juvenil en esta categoría'
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
        default=50,
        help_text='minimo numero de camisena juvenil'
    )
    max_number_youth_player = models.PositiveIntegerField(
        'Numero Maximo Juvenil',
        default=100,
        help_text='maximo numero de camisena juvenil'
    )
    min_number_player = models.PositiveIntegerField(
        'Numero Minimo',
        default=5,
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
    
    def __str__(self):
        return self.name
    
    def is_youth_player(self, player_age):
        """Determina si un jugador es juvenil según las reglas de la categoría."""
        if player_age is None:
            return False
            
        # Para SENIOR y FEMENINO: juvenil es menor de 18
        if self.name in ['SENIOR', 'FEMENINO']:
            return player_age < 18
        
        # Para MASTER: juvenil es entre 38-39 años
        if self.name == 'MASTER':
            return 38 <= player_age <= 39
            
        # Si hay rangos específicos definidos, usarlos
        if self.youth_min_age is not None and self.youth_max_age is not None:
            return self.youth_min_age <= player_age <= self.youth_max_age
            
        return False
