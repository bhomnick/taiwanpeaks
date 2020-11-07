from django.contrib import admin

from .models import Location, FeaturedRoute


@admin.register(FeaturedRoute)
class FeaturedRouteAdmin(admin.ModelAdmin):
    list_display = ['route', 'order']
    list_editable = ['order']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_short', 'slug']
    prepopulated_fields = {'slug': ('name',)}
