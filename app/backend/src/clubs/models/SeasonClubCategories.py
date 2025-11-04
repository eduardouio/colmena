from django.db import models
from common.BaseModel import BaseModel
from .Season import Season
from .ClubCategorie import ClubCategorie
from .Club import Club
from .Player import Player

class SeasonClubCategories(BaseModel):
	id = models.AutoField(primary_key=True)
	season = models.ForeignKey(
		Season,
		 on_delete=models.PROTECT,
	)
	club_categorie = models.ForeignKey(
		ClubCategorie,
		on_delete=models.PROTECT
	)
	winner = models.ForeignKey(
		Club,
		on_delete=models.PROTECT,
		null=True,
		blank=True
	)
	second = models.ForeignKey(
		Club,
		on_delete=models.PROTECT,
		null=True,
		blank=True
	)
	third = models.ForeignKey(
		Club,
		on_delete=models.PROTECT,
		null=True,
		blank=True
	)
	scoring_player = models.ForeignKey(
		Player,
		on_delete=models.PROTECT,
		null=True,
		blank=True
	)
	
	class Meta:
		verbose_name = 'Temporada Club Categoría'
		verbose_name_plural = 'Temporadas Club Categorías'
		ordering = ['-created_at']
		db_table = 'season_club_categories'
		