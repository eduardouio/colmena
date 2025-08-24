from django.contrib import admin

from .models.RegisterModel import Register


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = (
        'created_at', 'updated_at', 'id_user_created', 'id_user_updated'
    )
    list_filter = ('is_active', 'is_deleted', 'created_at')
    search_fields = ()
    ordering = ('-created_at',)
    list_per_page = 25


@admin.register(Register)
class RegisterAdmin(BaseModelAdmin):
    list_display = (
        'id', 'season', 'club', 'player', 'category', 'number', 'status',
        'is_requalification', 'have_pass', 'is_active', 'is_deleted'
    )
    search_fields = (
        'player__first_name', 'player__last_name', 'player__national_id',
        'club__name'
    )
    list_filter = BaseModelAdmin.list_filter + (
        'season', 'club', 'category', 'status', 'is_requalification', 'have_pass'
    )
