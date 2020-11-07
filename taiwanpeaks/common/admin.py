from django.contrib import admin

from .models import Location, FeaturedPeak, FeaturedRoute


@admin.register(FeaturedPeak)
class FeaturedPeakAdmin(admin.ModelAdmin):
    list_display = ['peak', 'order', 'name_override']
    list_editable = ['order', 'name_override']


@admin.register(FeaturedRoute)
class FeaturedRouteAdmin(admin.ModelAdmin):
    list_display = ['route', 'order']
    list_editable = ['order']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_short', 'slug']
    prepopulated_fields = {'slug': ('name',)}
