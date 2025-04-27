# Este archivo ahora importa de los módulos individuales para mantener compatibilidad
from .views.registro_aspirante_view import RegistroAspiranteView
from .views.success_view import SuccessView
from .views.error_view import ErrorView
from .views.registro_detail_view import RegistroDetailView
from .views.home_view import HomeView

# Mantener compatibilidad con imports antiguos
__all__ = [
    'RegistroAspiranteView',
    'SuccessView',
    'ErrorView',
    'RegistroDetailView',
    'HomeView'
]
