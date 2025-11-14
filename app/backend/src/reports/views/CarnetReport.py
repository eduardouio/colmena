from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from clubs.models.Register import Register
from datetime import date


class CarnetReport(TemplateView):
	template_name = "reports/carnet.html"
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		
		# Obtener el ID del registro desde la URL
		registro_id = self.request.GET.get('id')
		registro = get_object_or_404(Register, pk=registro_id)
		
		# Calcular edad del jugador
		edad = None
		if registro.player.birth_date:
			today = date.today()
			edad = today.year - registro.player.birth_date.year
			if today.month < registro.player.birth_date.month or \
			   (today.month == registro.player.birth_date.month and today.day < registro.player.birth_date.day):
				edad -= 1
		
		# URLs de las imágenes
		foto_url = registro.photo.url if registro.photo else ''
		logo_url = registro.club.logo.url if hasattr(registro.club, 'logo') and registro.club.logo else ''
		
		# Agregar datos al contexto
		context['registro'] = registro
		context['edad'] = edad
		context['foto_url'] = foto_url
		context['logo_url'] = logo_url
		
		return context