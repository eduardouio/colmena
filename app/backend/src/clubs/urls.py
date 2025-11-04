from django.urls import path
from .views.PlayersClubLists import PlayersClubListView
from .views.PlayerCreate import PlayerCreateView
from api.views.CheckPlayerExistView import CheckPlayerExistView
from .views.PlayerPresentation import player_register_presentation
from .views.PlayerSheet import player_sheet
from .views.IDPlayerSeason import player_id_card

app_name = 'clubs'

urlpatterns = [
    path('club/<int:club_id>/players/', PlayersClubListView.as_view(), name='players_list'),
    path('club/<int:club_id>/players/create/', PlayerCreateView.as_view(), name='player_create'),
    
    # API endpoints
    path('api/check-player/', CheckPlayerExistView.as_view(), name='api_check_player'),
    
    # Player Register Presentation
    path('register/<int:register_id>/presentation/', player_register_presentation, name='player_register_presentation'),
    
    # Player Sheet (Ficha imprimible)
    path('register/<int:register_id>/sheet/', player_sheet, name='player_sheet'),
    
    # Player ID Card (Carnet)
    path('register/<int:register_id>/card/', player_id_card, name='player_id_card'),
]