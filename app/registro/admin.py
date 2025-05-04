from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Club, CalificacionAspirante


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(CalificacionAspirante)
class CalificacionAspiranteAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'cedula', 'categoria', 'club', 'temporada', 'email', 'numero_jugador', 'created_at', 'acciones')
    list_filter = ('temporada', 'categoria', 'club', 'recalificacion', 'tiene_pases', 'created_at')
    search_fields = ('nombres', 'apellidos', 'cedula', 'email', 'numero_jugador')
    date_hierarchy = 'created_at'
    list_per_page = 25
    ordering = ('-created_at',)  # Ordenar por fecha de creación descendente
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
        ('Notas y Observaciones', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
    )

    def acciones(self, obj):
        """Muestra botones para ver carnet y descargar PDF."""
        ver_carnet = reverse('registro:ver_carnet', args=[obj.id])
        descargar_pdf = reverse('registro:descargar_pdf', args=[obj.id])
        
        return format_html(
            '<a class="button" href="{}" target="_blank" style="margin-right:10px;background-color:#1d91d0;color:white;padding:5px 10px;border-radius:4px;text-decoration:none;">Ver Carnet</a>'
            '<a class="button" href="{}" style="background-color:#28a745;color:white;padding:5px 10px;border-radius:4px;text-decoration:none;">Descargar PDF</a>',
            ver_carnet, descargar_pdf
        )
    
    acciones.short_description = 'Acciones'
    acciones.allow_tags = True
