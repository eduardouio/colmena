from django.db import models
from common.BaseModel import BaseModel
from .Club import Club
from .Categorie import Categorie


class ClubCategorie(BaseModel):
    """
    Modelo intermedio para la relación muchos a muchos entre Club y Category.
    Permite que un club tenga múltiples categorías y una categoría pueda estar en múltiples clubes.
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name='ID'
    )
    club = models.ForeignKey(
        Club,
        on_delete=models.PROTECT,
        verbose_name='club',
        related_name='club_categories'
    )
    
    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.PROTECT,
        verbose_name='categoría',
        related_name='club_categories'
    )
    
    
    class Meta:
        verbose_name = 'relación club-categoría'
        verbose_name_plural = 'relaciones club-categorías'
        unique_together = ('club', 'categorie')
    
    def __str__(self):
        return f"{self.club.name} - {self.categorie.name}"