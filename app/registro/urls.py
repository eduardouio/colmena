from django.urls import path
from .views import RegistroAspiranteView, SuccessView, ErrorView

app_name = 'registro'

urlpatterns = [
    path('', RegistroAspiranteView.as_view(), name='formulario'),
    path('exito/', SuccessView.as_view(), name='success'),
    path('error/', ErrorView.as_view(), name='error'),
]