from django.contrib import admin
from django.utils.html import format_html
from .models.Club import Club
from .models.Categorie import Categorie
from .models.Player import Player
from .models.Season import Season
from .models.Register import Register
from .models.ClubCategorie import ClubCategorie


class BaseModelAdmin(admin.ModelAdmin):
    """Configuración base para modelos que heredan de BaseModel."""
    readonly_fields = (
        'created_at', 'updated_at', 'id_user_created', 'id_user_updated',
        'get_created_by', 'get_updated_by'
    )
    list_filter = ('is_active', 'is_deleted', 'created_at')
    search_fields = ()  # Definir en subclase
    ordering = ('-created_at',)
    list_per_page = 25
    
    fieldsets = (
        ('Información Principal', {
            'fields': ()  # Sobrescribir en cada subclase
        }),
        ('Estado y Control', {
            'fields': ('is_active', 'is_deleted', 'notes'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_at', 'updated_at',
                'id_user_created', 'get_created_by',
                'id_user_updated', 'get_updated_by'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_created_by(self, obj):
        return obj.get_create_user()
    get_created_by.short_description = 'Creado por'
    
    def get_updated_by(self, obj):
        return obj.get_update_user()
    get_updated_by.short_description = 'Actualizado por'


@admin.register(Club)
class ClubAdmin(BaseModelAdmin):
    list_display = (
        'id', 'name', 'president', 'email', 'phone', 'is_active', 'is_deleted',
        'created_at', 'updated_at'
    )
    search_fields = (
        'name', 'president', 'email', 'vocal_a', 'vocal_b', 'aproved_by',
        'reviewed_by'
    )
    list_filter = BaseModelAdmin.list_filter + (
        'date_review', 'date_approval'
    )
    ordering = ('name',)
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Información del Club', {
            'fields': ('name', 'president', 'email', 'phone', 'address')
        }),
        ('Vocales y Aprobación', {
            'fields': ('vocal_a', 'vocal_b', 'reviewed_by', 'date_review', 
                      'aproved_by', 'date_approval'),
            'classes': ('collapse',)
        }),
        ('Estado y Control', {
            'fields': ('is_active', 'is_deleted', 'notes'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_at', 'updated_at',
                'id_user_created', 'get_created_by',
                'id_user_updated', 'get_updated_by'
            ),
            'classes': ('collapse',)
        }),
    )


@admin.register(Categorie)
class CategorieAdmin(BaseModelAdmin):
    list_display = (
        'id', 'name', 'description', 'min_age', 'max_players', 'is_active',
        'is_deleted', 'created_at', 'updated_at'
    )
    list_editable = ('is_active',)
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'is_deleted', 'created_at', 'name')
    ordering = ('name',)
    
    fieldsets = (
        ('Información de Categoría', {
            'fields': ('name', 'description', 'min_age')
        }),
        ('Configuración de Jugadores', {
            'fields': ('max_players', 'max_youth_player', 
                      'youth_min_age', 'youth_max_age',  # Añadir estos campos
                      'min_number_youth_player', 'max_number_youth_player',
                      'min_number_player', 'max_number_player')
        }),
        ('Estado y Control', {
            'fields': ('is_active', 'is_deleted', 'notes'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_at', 'updated_at',
                'id_user_created', 'get_created_by',
                'id_user_updated', 'get_updated_by'
            ),
            'classes': ('collapse',)
        }),
    )


@admin.register(Player)
class PlayerAdmin(BaseModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'national_id', 'email', 'birth_date',
        'has_transfers', 'is_active', 'is_deleted', 'created_at'
    )
    search_fields = ('first_name', 'last_name', 'national_id', 'email')
    list_filter = ('has_transfers', 'is_active', 'is_deleted', 'created_at')
    ordering = ('last_name', 'first_name')
    list_editable = ('is_active', 'has_transfers')
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'national_id', 'birth_date')
        }),
        ('Información de Contacto', {
            'fields': ('email',)
        }),
        ('Estado Deportivo', {
            'fields': ('has_transfers',)
        }),
        ('Estado y Control', {
            'fields': ('is_active', 'is_deleted', 'notes'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_at', 'updated_at',
                'id_user_created', 'get_created_by',
                'id_user_updated', 'get_updated_by'
            ),
            'classes': ('collapse',)
        }),
    )


@admin.register(Season)
class SeasonAdmin(BaseModelAdmin):
    list_display = (
        'id', 'name', 'categorie', 'start_date', 'end_date', 
        'is_active', 'is_deleted', 'created_at'
    )
    search_fields = ('name', 'categorie__name')
    list_filter = ('is_active', 'is_deleted', 'start_date', 'end_date', 'categorie')
    date_hierarchy = 'start_date'
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Información de Temporada', {
            'fields': ('name', 'categorie', 'start_date', 'end_date')
        }),
        ('Resultados', {
            'fields': ('winner', 'second', 'third', 'scoring_player'),
            'classes': ('collapse',)
        }),
        ('Estado y Control', {
            'fields': ('is_active', 'is_deleted', 'notes'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_at', 'updated_at',
                'id_user_created', 'get_created_by',
                'id_user_updated', 'get_updated_by'
            ),
            'classes': ('collapse',)
        }),
    )


@admin.register(Register)
class RegisterAdmin(BaseModelAdmin):
    list_display = (
        'id', 'player', 'club', 'season', 'number', 'status',
        'is_requalification', 'have_pass', 'is_active', 'is_deleted', 'created_at'
    )
    list_filter = (
        'status', 'is_requalification', 'have_pass', 'club', 
        'season__categorie', 'is_active', 'is_deleted'
    )
    search_fields = (
        'player__first_name', 'player__last_name', 'player__national_id',
        'club__name', 'season__name', 'number'
    )
    list_select_related = ('player', 'club', 'season')
    list_editable = ('status', 'is_active')
    
    fieldsets = (
        ('Información de Registro', {
            'fields': ('season', 'club', 'player', 'number')
        }),
        ('Documentos', {
            'fields': ('minor_authorization', 'photo', 'id_document'),
            'classes': ('collapse',)
        }),
        ('Estado de Registro', {
            'fields': ('status', 'is_requalification', 'have_pass', 'before_club')
        }),
        ('Estado y Control', {
            'fields': ('is_active', 'is_deleted', 'notes'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_at', 'updated_at',
                'id_user_created', 'get_created_by',
                'id_user_updated', 'get_updated_by'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def view_on_site(self, obj):
        # Opcional: Añadir un enlace para ver documentos si es necesario
        if obj.minor_authorization or obj.photo or obj.id_document:
            return f'/admin/view_documents/{obj.id}/'
        return None


@admin.register(ClubCategorie)
class ClubCategorieAdmin(BaseModelAdmin):
    list_display = (
        'id', 'club', 'categorie', 'is_active', 'is_deleted', 
        'created_at', 'updated_at'
    )
    search_fields = ('club__name', 'categorie__name')
    list_filter = ('is_active', 'is_deleted', 'created_at', 'categorie', 'club')
    list_select_related = ('club', 'categorie')
    ordering = ('club__name', 'categorie__name')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Relación Club-Categoría', {
            'fields': ('club', 'categorie')
        }),
        ('Estado y Control', {
            'fields': ('is_active', 'is_deleted', 'notes'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': (
                'created_at', 'updated_at',
                'id_user_created', 'get_created_by',
                'id_user_updated', 'get_updated_by'
            ),
            'classes': ('collapse',)
        }),
    )
