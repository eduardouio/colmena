from django.contrib import admin

from .models.ClubModel import Club


class BaseModelAdmin(admin.ModelAdmin):
    """Configuración base para modelos que heredan de BaseModel."""
    readonly_fields = (
        'created_at', 'updated_at', 'id_user_created', 'id_user_updated'
    )
    list_filter = ('is_active', 'is_deleted', 'created_at')
    search_fields = ()  # Definir en subclase
    ordering = ('-created_at',)
    list_per_page = 25


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
