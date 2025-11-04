from django.db import models

from common.BaseModel import BaseModel


class Season(BaseModel):
    id = models.AutoField(
        primary_key=True
    )
    name = models.CharField(
        'nombre',
        max_length=120, unique=True
    )
    start_date = models.DateField(
        'fecha inicio'
    )
    end_date = models.DateField(
        'fecha fin'
    )
    class Meta:
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'
        ordering = ['-start_date']

    def __str__(self):
        return self.name
