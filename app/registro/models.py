from django.db import models
from datetime import date
from django.core.exceptions import ValidationError


class Club(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class CalificacionAspirante(models.Model):
    CATEGORIAS = [
        ('niños', 'Niños'),
        ('femenino', 'Femenino'),
        ('senior', 'Senior'),
        ('master', 'Master'),
    ]

    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado'),
        ('Rechazado', 'Rechazado'),
    ]

    email = models.EmailField()
    temporada = models.CharField(max_length=20)
    club = models.ForeignKey(Club, on_delete=models.PROTECT)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField()
    numero_jugador = models.PositiveIntegerField()
    tiene_pases = models.BooleanField()
    autorizacion_menor = models.FileField(
        upload_to='autorizaciones/', null=True, blank=True)
    foto_fondo_claro = models.FileField(upload_to='fotos_claras/')
    foto_cedula = models.FileField(upload_to='cedulas/')
    recalificacion = models.BooleanField()

    # Campos nuevos
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=10, choices=ESTADOS, default='Pendiente')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.cedula})"

    def clean(self):
        super().clean()
        today = date.today()
        age = today.year - self.fecha_nacimiento.year - \
            ((today.month, today.day) <
             (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

        if self.categoria == 'niños':
            if not (7 <= age <= 11):
                raise ValidationError(
                    'La categoría "Niños" requiere una edad entre 7 y 11 años.')

        elif self.categoria in ['senior', 'femenino']:
            if age < 18 and self.numero_jugador < 50:
                raise ValidationError(
                    'Los menores de 18 años deben usar un número superior a 50 en la categoría "Senior" o "Femenino".')
            if age >= 18 and self.numero_jugador > 49:
                raise ValidationError(
                    'Los mayores de 18 años deben usar un número menor o igual a 49 en la categoría "Senior" o "Femenino".')

        elif self.categoria == 'master':
            if age < 39 and self.numero_jugador < 50:
                raise ValidationError(
                    'Los menores de 40 años deben usar un número superior a 50 en la categoría "Master".')