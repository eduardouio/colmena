from django.urls import path
from .views.PlayersClubLists import PlayersClubListView

app_name = 'clubs'  # Este es el namespace que debe estar definido

urlpatterns = [
    # Agregar aquí otras URLs existentes del módulo clubs si las hay
    path('club/<int:club_id>/players/', PlayersClubListView.as_view(), name='players_list'),
]