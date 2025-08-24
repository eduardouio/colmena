from django.contrib import admin

from .models.PlayerModel import Player


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = (
        'created_at', 'updated_at', 'id_user_created', 'id_user_updated', 'is_minor'
    )
    list_filter = ('is_active', 'is_deleted', 'is_minor', 'created_at')
    search_fields = ()
    ordering = ('last_name', 'first_name')
    list_per_page = 25


@admin.register(Player)
class PlayerAdmin(BaseModelAdmin):
    list_display = (
        'id', 'last_name', 'first_name', 'national_id', 'email', 'birth_date',
        'is_minor', 'has_transfers', 'is_active', 'is_deleted'
    )
    search_fields = (
        'first_name', 'last_name', 'national_id', 'email'
    )
    list_filter = BaseModelAdmin.list_filter + (
        'has_transfers',
    )
