from django.contrib import admin
from django.utils.html import format_html
from .models.Club import Club
from .models.Categorie import Categorie
from .models.Player import Player
from .models.Season import Season
from .models.Register import Register


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


@admin.register(Categorie)
class CategorieAdmin(BaseModelAdmin):
    list_display = (
        'id', 'name', 'description', 'min_age', 'max_players', 'is_active',
        'created_at', 'updated_at'
    )
    list_editable = ('is_active',)
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'is_deleted', 'created_at')
    ordering = ('name',)



@admin.register(Player)
class PlayerAdmin(BaseModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'national_id', 'email', 'birth_date',
        'has_transfers', 'is_active', 'created_at'
    )
    search_fields = ('first_name', 'last_name', 'national_id', 'email')
    list_filter = ('has_transfers', 'is_active', 'is_deleted')
    ordering = ('last_name', 'first_name')


@admin.register(Season)
class SeasonAdmin(BaseModelAdmin):
    list_display = (
        'id', 'name', 'start_date', 'end_date', 'is_active', 'created_at'
    )
    search_fields = ('name',)
    list_filter = ('is_active', 'start_date', 'end_date')
    date_hierarchy = 'start_date'



@admin.register(Register)
class RegisterAdmin(BaseModelAdmin):
    list_display = (
        'id', 'player', 'club', 'season', 'number', 'status',
        'is_requalification', 'have_pass', 'before_club', 'created_at'
    )
    list_filter = (
        'status', 'is_requalification', 'have_pass', 'club', 'season__categorie', 'is_active'
    )
    search_fields = (
        'player__first_name', 'player__last_name', 'player__national_id',
        'club__name', 'season__name', 'number'
    )
    list_select_related = ('player', 'club', 'season')
    raw_id_fields = ('player', 'club', 'season')
    
    def view_on_site(self, obj):
        # Opcional: Añadir un enlace para ver documentos si es necesario
        if obj.minor_authorization or obj.photo or obj.id_document:
            return f'/admin/view_documents/{obj.id}/'
        return None
