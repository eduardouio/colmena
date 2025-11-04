from django.urls import path
from .views.PlayersClubLists import PlayersClubListView

app_name = 'clubs'

urlpatterns = [
    path('club/<int:club_id>/players/', PlayersClubListView.as_view(), name='players_list'),
]