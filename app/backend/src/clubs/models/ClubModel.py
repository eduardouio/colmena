from django.db import models
from common.BaseModel import BaseModel
from accounts.models.CustomUserModel import CustomUserModel


class Club(BaseModel):
    """Modelo de Club."""
    id = models.AutoField(
        primary_key=True
    )
    name = models.CharField(
        'nombre',
        max_length=100,
        unique=True,
    )
    president = models.CharField(
        'presidente',
        max_length=100,
        blank=True,
        null=True
    )
    email = models.EmailField(
        'email',
        unique=True,
        blank=True,
        null=True
    )
    phone = models.CharField(
        'teléfono',
        max_length=15,
        blank=True,
        null=True
    )
    vocal_a = models.CharField(
        'Vocal A',
        max_length=100
    )
    vocal_b = models.CharField(
        'Vocal B',
        max_length=100,
    )
    aproved_by = models.CharField(
        'aprobado por',
        max_length=100,
        blank=True,
        null=True
    )
    reviewed_by = models.CharField(
        'revisado por',
        max_length=100,
        blank=True,
        null=True
    )
    date_review = models.DateField(
        'fecha de revisión',
        null=True,
        blank=True,
    )
    date_approval = models.DateField(
        'fecha de aprobación',
        null=True,
        blank=True
    )
    users = models.ForeignKey(
        CustomUserModel,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text='Usuario asociado al club.'
    )

    class Meta:
        verbose_name = 'Club'
        verbose_name_plural = 'Clubs'

    def __str__(self) -> str:
        return self.name
