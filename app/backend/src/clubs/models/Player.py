from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

from common.BaseModel import BaseModel


class Player(BaseModel):
    id = models.AutoField(
        primary_key=True
    )
    first_name = models.CharField(
        'Nombres',
        max_length=100
    )
    last_name = models.CharField(
        'Apellidos',
        max_length=100
    )
    national_id = models.CharField(
        'Cédula',
        max_length=10,
        unique=True
    )
    email = models.EmailField(
        'Correo electrónico',
        max_length=100,
        unique=True
    )
    birth_date = models.DateField(
        'Fecha de nacimiento',
        blank=True,
        null=True
    )
    has_transfers = models.BooleanField(
        'tiene pases',
        default=False
    )

    class Meta:
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'
        ordering = ['last_name', 'first_name', 'pk']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

