from django.contrib import admin

from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_short', 'slug']
    prepopulated_fields = {'slug': ('name',)}
