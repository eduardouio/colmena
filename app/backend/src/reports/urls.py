from django.urls import path
from reports.views.AllCarnetsReport import AllCarnetsReport
from reports.views.CarnetReport import CarnetReport
from reports.views.PDFAllCarnetsReport import PDFAllCarnetsReport
from reports.views.PDFCarnetreport import PDFCarnetreport

app_name = 'reports'

urlpatterns = [
    # Vistas HTML
    path('carnet/<int:pk>/', CarnetReport.as_view(), name='carnet'),
    path('carnets/categoria/<int:categoria_id>/', AllCarnetsReport.as_view(), name='carnets_categoria'),
    
    # Vistas PDF
    path('pdf/carnet/<int:registro_id>/', PDFCarnetreport.as_view(), name='pdf_carnet'),
    path('pdf/carnets/categoria/<int:categoria_id>/', PDFAllCarnetsReport.as_view(), name='pdf_carnets_categoria'),
]
