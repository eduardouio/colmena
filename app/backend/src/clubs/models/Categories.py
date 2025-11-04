from django.db import models
from common.BaseModel import BaseModel


class Category(BaseModel):
    """
    Modelo para las categorías de los clubes.
    
    Las categorías pueden ser: FEMENINO, MASTER, SENIOR, etc.
    """
    id = models.AutoField(
        primary_key=True,
        verbose_name='ID'
    )
    
    name = models.CharField(
        'nombre',
        max_length=50,
        unique=True,
        help_text='Nombre de la categoría (ej: FEMENINO, MASTER, SENIOR)'
    )
    
    code = models.CharField(
        'código',
        max_length=10,
        unique=True,
        help_text='Código corto de la categoría (ej: FEM, MAS, SEN)'
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
    
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
        db_table = 'categories'
    
    def __str__(self):
        return self.name
