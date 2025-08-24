from django.contrib import admin

from .models.SeasonModel import Season


class BaseModelAdmin(admin.ModelAdmin):
    readonly_fields = (
        'created_at', 'updated_at', 'id_user_created', 'id_user_updated'
    )
    list_filter = ('is_active', 'is_deleted', 'created_at')
    search_fields = ()
    ordering = ('-start_date',)
    list_per_page = 25


@admin.register(Season)
class SeasonAdmin(BaseModelAdmin):
    list_display = (
        'id', 'name', 'start_date', 'end_date', 'is_active', 'is_deleted'
    )
    search_fields = ('name',)
    list_filter = BaseModelAdmin.list_filter + (
        'start_date', 'end_date'
    )
