from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Photo


@admin.register(Photo)
class PhotoAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ['attr_title', 'attr_license', 'get_preview']

    def get_preview(self, obj):
        return obj.thumbnail_preview
    get_preview.short_description = 'Image preview'
    get_preview.allow_tags = True
