Instalación rápida Colmena:
```bash
cd app/backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requeriments.txt

./manage.py makemigrations accounts clubs
./manage.py migrate
./manage.py createsuperuser --email eduardouio7@gmail.com
./manage.py runserver
```
