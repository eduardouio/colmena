from django.urls import path
from reports.views.AllCarnetsReport import AllCarnetsReport
from reports.views.CarnetReport import CarnetReport

app_name = 'reports'

urlpatterns = [
    path('carnet/<int:pk>/', CarnetReport.as_view(), name='carnet'),
    path('carnets/', AllCarnetsReport.as_view(), name='all_carnets'),
]
