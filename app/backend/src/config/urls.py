from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views.HomeTempView import HomeTempView
from accounts.views.LoginTempView import LoginTempView
from accounts.views.LoguoutRedView import LogoutRedView
from clubs.views.LandingPage import LandingPageView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('home/', HomeTempView.as_view(), name='home'),
    path('login/', LoginTempView.as_view(), name='login'),
    path('logout/', LogoutRedView.as_view(), name='logout'),
    path('grappelli/', include('grappelli.urls')),  # grappelli URLS - debe ir ANTES del admin
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('api/', include('api.urls', namespace='api')),
    path('clubs/', include('clubs.urls', namespace='clubs')),
    path('reports/', include('reports.urls', namespace='reports')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
