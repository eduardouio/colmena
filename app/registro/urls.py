from django.urls import path
from .views import (
    RegistroAspiranteView,
    SuccessView,
    ErrorView,
    RegistroDetailView,
    HomeView,
    descargar_registro_pdf,
    preview_registro,
    descargar_pdf,
    buscar_ficha,
    VistaCarnet,
    VistaMasivaCarnet,
)

app_name = 'registro'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('registro/', RegistroAspiranteView.as_view(), name='formulario'),
    path('exito/<int:pk>/', SuccessView.as_view(), name='success'),
    path('error/', ErrorView.as_view(), name='error'),
    path('ver/<int:pk>/', RegistroDetailView.as_view(), name='ver_registro'),
    path('descargar_pdf/<int:pk>/', descargar_registro_pdf, name='descargar_registro_pdf'),
    path('preview/<int:pk>/', preview_registro, name='preview_registro'),
    path('descargar/<int:pk>/', descargar_pdf, name='descargar_pdf'),
    path('api/buscar-ficha/', buscar_ficha, name='buscar_ficha'),
    path('carnet/<int:pk>/', VistaCarnet.as_view(), name='ver_carnet'),
    path('carnet-masivo/', VistaMasivaCarnet.as_view(), name='ver_carnet_masivo'),
]
