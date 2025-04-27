from .registro_aspirante_view import RegistroAspiranteView
from .success_view import SuccessView
from .error_view import ErrorView
from .registro_detail_view import RegistroDetailView
from .home_view import HomeView
from .views import descargar_registro_pdf, preview_registro
from .report import descargar_pdf

__all__ = [
    'RegistroAspiranteView',
    'SuccessView',
    'ErrorView',
    'RegistroDetailView',
    'HomeView',
    'descargar_registro_pdf',
    'preview_registro',
    'descargar_pdf'
]
