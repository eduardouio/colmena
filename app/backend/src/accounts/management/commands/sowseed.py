from django.db import connection
import secrets
from datetime import datetime
from django.core.management.base import BaseCommand
from clubs.models.Club import Club
from clubs.models.Categorie import Categorie
from clubs.models.ClubCategorie import ClubCategorie
from clubs.models.Season import Season
from clubs.models.Player import Player
from accounts.models.CustomUserModel import CustomUserModel
from accounts.models.Licence import License

clubs ="""BARCELONA T.L,barcelonatl@colmenaec.com
DINAMO,dinamo@colmenaec.com
GENOVA,genova@colmenaec.com
INDEPENDIENTE DE LAS CASAS,independientelascasas@colmenaec.com
INDEPENDIENTE,independiente@colmenaec.com
J.L,jl@colmenaec.com
NETHERLANDS,netherlands@colmenaec.com
NEW GIRLS,newgirls@colmenaec.com
NEW KIDS,newkids@colmenaec.com
NUEVA GENERACION,nuevageneracion@colmenaec.com
MANCHESTER,manchester@colmenaec.com
ROTTERDAM,rotterdam@colmenaec.com
SAN CARLOS,sancarlos@colmenaec.com
VALLADOLID,valladolid@colmenaec.com
VODARS,vodars@colmenaec.com
ARSENAL,arsenal@colmenaec.com
ATLETICO A,atleticoa@colmenaec.com
ATLETICO MADRID,atleticomadrid@colmenaec.com
ATLETICO PHARMA,atleticopharma@colmenaec.com
BARON ROJO,baronrojo@colmenaec.com
CATOLICA JUVENIL,catolicajuvenil@colmenaec.com
CRUCEIRO,cruceiro@colmenaec.com
CHAPECOENSE,chapecoense@colmenaec.com
FIORENTINA,fiorentina@colmenaec.com
GALAX,galax@colmenaec.com
GOLDEN WARRIORS,goldenwarriors@colmenaec.com
JUVENTUS,juventus@colmenaec.com
LIVERPOOL,liverpool@colmenaec.com
LIBERTAD F.C,libertadfc@colmenaec.com
MAFICK F.C,mafickfc@colmenaec.com
METALES,metales@colmenaec.com
MEXICO,mexico@colmenaec.com
MILAN,milan@colmenaec.com
MINERVEN,minerven@colmenaec.com
NUEVA ALIANZA,nuevaalianza@colmenaec.com
OLMEDO JR.,olmedojr@colmenaec.com
PELOTEROS,peloteros@colmenaec.com   
PIBES,pibes@colmenaec.com
P.S.G.,psg@colmenaec.com
REDIMI 2,redimi2@colmenaec.com
RIVER PLATE F7,riverplatef7@colmenaec.com
ROSARIO CENTRAL,rosariocentral@colmenaec.com
SPORTING C.G,sportingcg@colmenaec.com
SOLO PANAS,solopanas@colmenaec.com
LAZIO,lazio@colmenaec.com
RACING,racing@colmenaec.com
CERRO PORTEÑO,cerroporteno@colmenaec.com
TALLERES SAENZ,talleressaenz@colmenaec.com
HURACAN,huracan@colmenaec.com
ATLETICO MINEIROS,atleticomineiros@colmenaec.com
SPORT BOYS FC,sportboysfc@colmenaec.com
Q LEONES,qleones@colmenaec.com
AUQUITAS,auquitas@colmenaec.com
LA LEYENDA,laleyenda@colmenaec.com
LIGA LDU,liga_ldu@colmenaec.com
KOSMOS FUTBOL CLUB,kosmos_futbol_club@colmenaec.com
BARCELONA T.L FEMENINO,barcelonatl_f@colmenaec.com
DINAMO FEMENINO,dinamo_f@colmenaec.com
NUEVA GENERACION FEMENINO,nuevageneracion_f@colmenaec.com
SAN CARLOS FEMENINO,sancarlos_f@colmenaec.com
VALLADOLID FEMENINO,valladolid_f@colmenaec.com
VODARS FEMENINO,vodars_f@colmenaec.com
ATLETICO A MASTER,atleticoa_m@colmenaec.com
LIBERTAD F.C MASTER,libertadfc_m@colmenaec.com
MINERVEN MASTER,minerven_m@colmenaec.com
INDEPENDIENTE FEMENINO,independiente_f@colmenaec.com
NEW KIDS FEMENINO,newkids_f@colmenaec.com
INDEPENDIENTE MASTER,independiente_m@colmenaec.com
NEW KIDS MASTER,newkids_m@colmenaec.com
"""

user_admins = """EDUARDO,VILLOTA,eduardouio7@gmail.com
ALEXANDRA,CATAGÑA,calificaciones1@colmenaec.com
GABRIELA,ACONDA,calificaciones2@colmenaec.com
DIEGO,IZA,calificaciones@colmenaec.com
"""

class Command(BaseCommand):
    help = 'Crea datos de prueba'
    
    def handle(self, *args, **kwargs):
        self.createUsers()
        self.createLicenses()
        self.create_clubs()
        self.create_categories()
        self.create_club_categories()
        self.create_seasons()

    def createUsers(self):
        all_users = CustomUserModel.objects.all()
        if all_users.exists():
            print('Los usuarios ya existen, se omite la creación de superusuarios.')
            return
        
        for line in user_admins.splitlines():
            line = line.strip()
            if not line:
                continue
                
            # Split the line and ensure we have exactly 3 parts
            parts = [part.strip() for part in line.split(',', 2)]
            if len(parts) != 3:
                self.stdout.write(self.style.WARNING(f'Skipping invalid line: {line}'))
                continue
                
            first_name, last_name, email = parts
            if not all([first_name, last_name, email]):
                self.stdout.write(self.style.WARNING(f'Skipping line with missing data: {line}'))
                continue
                
            try:
                user = CustomUserModel.objects.create_superuser(
                    first_name=first_name,
                    last_name=last_name,
                    email=email.lower(),
                    password='Comision2025*',
                    is_staff=True,
                    is_superuser=True
                )
                user.is_active = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating user {email}: {str(e)}'))
            print(f'Usuarios Admin {email} creado')
        
        for line in clubs.splitlines():
            if line.strip() == '':
                continue
            name, email = line.split(',')
            user = CustomUserModel.objects.create_user(
                first_name=name,
                last_name='',
                email=email.strip().lower(),
                password='Colmena2025*',
                is_staff=False,
                is_superuser=False
            )
            print(f'Usuario {email} creado')

    def createLicenses(self):
        all_licenses = License.objects.all()
        if all_licenses.exists():
            print('Las licencias ya existen, se omite la creación de licencias.')
            return
        
        users = CustomUserModel.objects.all()
        for user in users:
            license = License(
                license_key=secrets.token_hex(16),
                activated_on=datetime.now(),
                expires_on=datetime(2026, 12, 31),
                enterprise='COLMENA',
                url_server='https://colmenaec.com',
                user=user,
                is_active=True
            )
            license.save()
            print(f'Licencia para {user.email} creada')

    def create_clubs(self):
        all_clubs = Club.objects.all()
        if all_clubs.exists():
            print('Los clubs ya existen, se omite la creación de clubs.')
            return
        
        for line in clubs.splitlines():
            if line.strip() == '':
                continue
            name, email = [part.strip() for part in line.split(',')]
            user = CustomUserModel.objects.filter(email=email.lower()).first()
            if not user:
                print(f'No se encontró usuario para el club en la línea: {line}')
                raise Exception('Usuario no encontrado para club')
            club = Club(
                name=name,
                email=email,
                users=user
            )
            club.save()
            print(f'Club {name} creado')

    def create_categories(self):
        all_categories = Categorie.objects.all()
        if all_categories.exists():
            print('Las categorías ya existen, se omite la creación de categorías.')
            return

        categories = ["SENIOR", "FEMENINO", "MASTER"]
        for category_name in categories:
            category, created = Categorie.objects.get_or_create(
                name=category_name,
                min_age=12 if category_name != 'MASTER' else 38,
                max_youth_player=20 if category_name != 'MASTER' else 1,
            )
            if created:
                category.save()
                print(f'Categoría {category_name} creada')

    def create_club_categories(self):
        all_club_categories = ClubCategorie.objects.all()
        if all_club_categories.exists():
            print('Las relaciones Club-Categoría ya existen, se omite la creación de las mismas.')
            return

        clubs = Club.objects.all()
        categories = Categorie.objects.all()
        for club in clubs:
            for category in categories:
                try:
                    club_category, created = ClubCategorie.objects.get_or_create(
                        club=club,
                        categorie=category,
                        defaults={
                            'club': club,
                            'categorie': category
                        }
                    )
                    if created:
                        print(f'Relación Club-Categoría {club.name} - {category.name} creada')
                    else:
                        print(f'Relación Club-Categoría {club.name} - {category.name} ya existía')
                except Exception as e:
                    print(f'Error creando relación para {club.name} - {category.name}: {str(e)}')

    def create_seasons(self):
        all_seasons = Season.objects.all()
        if all_seasons.exists():
            print('Las temporadas ya existen, se omite la creación de temporadas.')
            return

        categories = Categorie.objects.all()
        for category in categories:
            season_name = f"Temporada {category.name} 2024"
            season, created = Season.objects.get_or_create(
                name=season_name,
                categorie=category,
                start_date="2024-04-01",
                end_date="2025-04-30"
            )
            if created:
                season.save()
                print(f'Temporada {season_name} creada')

