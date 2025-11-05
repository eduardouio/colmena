Instalación rápida Colmena:
```bash

sudo systemctl daemon-reload &&
sudo systemctl restart colmena.service &&
sudo systemctl status colmena.service 
sudo systemctl restart nginx.service



cd app/backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requeriments.txt

./manage.py makemigrations accounts clubs &&
./manage.py migrate &&
./manage.py sowseed &&
./manage.py loadPlayers &&
./manage.py loadFemaleCategory &&
./manage.py loadMaleCategory &&
./manage.py runserver


./manage.py makemigrations accounts clubs
./manage.py migrate
./manage.py sowseed
./manage.py loadPlayers
./manage.py loadFemaleCategory
./manage.py loadMaleCategory
./manage.py runserver
```
