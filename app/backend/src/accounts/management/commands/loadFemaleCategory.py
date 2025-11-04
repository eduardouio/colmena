from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import connection

from clubs.models.Player import Player
from clubs.models.Categorie import Categorie
from clubs.models.Club import Club
from clubs.models.Season import Season


SQL_INSERT = """
INSERT INTO public.clubs_register (
	season_id,
	club_id,
	player_id,
	"number",
	minor_authorization,
	photo,
	id_document,
	have_pass,
	created_at,
	updated_at,
	status,
	is_active,
	is_deleted,
	id_user_created,
	id_user_updated,
	is_requalification
)VALUES
"""

class Command(BaseCommand):
	help = 'Load players from a CSV file'

	def handle(self,*args,**options):
		file = open('common/data/female_categorie.csv','r')
		lines = file.readlines()
		lines = [i.strip().split(',') for i in lines]

		season = Season.objects.get(name='Temporada FEMENINO 2024')

		for i,line in zip(range(len(lines[1:])),lines[1:]):
			new_player = Player.get_by_national_id(line[1])
			if not new_player:
				raise Exception(f'R{i}No se encontró la jugadora con cédula {line[1]}')

			club = Club.get_by_name(name=line[0].upper())
			if not club:
				raise Exception(f'R{i}No se encontró el club con nombre {line[0]}')

			now = datetime.now()
			line_sql = ("{},{},{},{},{},'{}','{}',{},'{}','{}','APROBADO',true,false,1,1,false").format(
				season.id,
				club.id,
				new_player.id,
				line[2],
				'null' if len(line[3]) == 0 else f"'{line[3]}'",
				line[4],
				line[5],
				'false' if line[6] == 0 else 'true',
				now.strftime('%Y-%m-%d %H:%M:%S'),
				now.strftime('%Y-%m-%d %H:%M:%S')
			)
			sql = SQL_INSERT + f"({line_sql});"
			print(sql)
			with connection.cursor() as cursor:
				cursor.execute(sql)
				print(f'R{i} Registro de jugadora {new_player.full_name} {new_player.national_id} en club {club.name} insertado.')
		file.close()
		