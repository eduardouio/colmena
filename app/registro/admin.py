from django.contrib import admin
from .models import Club, CalificacionAspirante

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)

@admin.register(CalificacionAspirante)
class CalificacionAspiranteAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'cedula', 'categoria', 'club', 'temporada', 'email', 'numero_jugador', 'created_at')
    list_filter = ('temporada', 'categoria', 'club', 'recalificacion', 'tiene_pases', 'created_at')
    search_fields = ('nombres', 'apellidos', 'cedula', 'email', 'numero_jugador')
    date_hierarchy = 'created_at'
    list_per_page = 25
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombres', 'apellidos', 'cedula', 'fecha_nacimiento', 'email')
        }),
        ('Información Deportiva', {
            'fields': ('temporada', 'club', 'categoria', 'numero_jugador', 'recalificacion', 'tiene_pases')
        }),
        ('Documentos', {
            'fields': ('foto_fondo_claro', 'foto_cedula', 'autorizacion_menor')
        }),
    )
