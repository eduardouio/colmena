from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

from common.BaseModel import BaseModel


class Player(BaseModel):
    """Modelo de jugador (versión simplificada).

    Campos actualmente definidos por el usuario:
        first_name, last_name, national_id, email, birth_date,
        photo, id_document, has_transfers.
    """
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
    is_minor = models.BooleanField(
        'es menor de edad',
        default=False,
        editable=False,
        help_text='Se calcula automáticamente desde birth_date.'
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

    def clean(self):
        super().clean()

        # Normalizar espacios en nombres
        if self.first_name:
            self.first_name = ' '.join(self.first_name.split())
        if self.last_name:
            self.last_name = ' '.join(self.last_name.split())

        # Validación cédula: 10 dígitos.
        if self.national_id and (
            len(self.national_id) != 10 or not self.national_id.isdigit()
        ):
            raise ValidationError({
                'national_id': 'La cédula debe tener exactamente 10 dígitos numéricos.'
            })

        # Fecha nacimiento / edad
        if self.birth_date:
            today = date.today()
            if self.birth_date > today:
                raise ValidationError({
                    'birth_date': 'La fecha de nacimiento no puede ser futura.'
                })
            age = (
                today.year
                - self.birth_date.year
                - int((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
            )
            if age > 100:
                raise ValidationError({
                    'birth_date': 'Edad mayor a 100 años no permitida (verificar dato).'
                })
            # Set automático de is_minor
            self.is_minor = age < 18
        else:
            # Sin fecha de nacimiento -> no se puede determinar, mantener False
            self.is_minor = False

    def save(self, *args, **kwargs):
        # Asegura consistencia (clean puede no llamarse siempre en código directo)
        self.clean()
        return super().save(*args, **kwargs)
