from django.contrib import admin

from .models import Peak


@admin.register(Peak)
class PeakAdmin(admin.ModelAdmin):
    list_display = ['name', 'rank', 'name_zh', 'get_preview']
    search_fields = ['name', 'name_zh']
    ordering = ['rank']
    raw_id_fields = ['list_photo']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['locations']

    def get_preview(self, obj):
        return obj.list_photo.thumbnail_preview
    get_preview.short_description = 'Image preview'
    get_preview.allow_tags = True
