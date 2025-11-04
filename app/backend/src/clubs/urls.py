from django.urls import path
from .views.PlayersClubLists import PlayersClubListView
from .views.PlayerCreate import PlayerCreateView
from api.views.CheckPlayerExistView import CheckPlayerExistView

app_name = 'clubs'

urlpatterns = [
    path('club/<int:club_id>/players/', PlayersClubListView.as_view(), name='players_list'),
    path('club/<int:club_id>/players/create/', PlayerCreateView.as_view(), name='player_create'),
    
    # API endpoints
    path('api/check-player/', CheckPlayerExistView.as_view(), name='api_check_player'),
]