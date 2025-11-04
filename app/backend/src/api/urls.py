from django.urls import path
from .views.CheckPlayerNumberView import CheckPlayerNumberView
from .views.CheckPlayerExistView import CheckPlayerExistView

app_name = 'api'



urlpatterns = [
    path('check-player-number/', CheckPlayerNumberView.as_view(), name='check_player_number'),
    path('check-player-exists/', CheckPlayerExistView.as_view(), name='check_player_exists'),
]

