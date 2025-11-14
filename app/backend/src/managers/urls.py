from django.urls import path
from managers.views.PlayersRegister import PlayersRegister

app_name = 'managers'

urlpatterns = [
	path('', PlayersRegister.as_view(), name='players_registers'),
]