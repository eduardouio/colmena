from django.core.management.base import BaseCommand
from django.db import connection



class Command(BaseCommand):
	help = 'Load players from a CSV file'

	def handle(self, *args, **options):
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM players")
			players = cursor.fetchall()
			for player in players:
				self.stdout.write(str(player))