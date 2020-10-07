from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Route, RouteCarouselPhoto, RouteItinerary, \
    RouteItineraryPhoto, RouteItineraryPoint, RouteCabin, Cabin


@admin.register(Cabin)
class CabinInline(AdminImageMixin, admin.ModelAdmin):
    list_display = ['name', 'name_zh', 'get_preview']
    ordering = ['name']
    raw_id_fields = ['photo']

    def get_preview(self, obj):
        return obj.photo.thumbnail_preview
    get_preview.short_description = 'Image preview'
    get_preview.allow_tags = True


class RouteCarouselPhotoInline(AdminImageMixin, admin.TabularInline):
    model = RouteCarouselPhoto
    ordering = ['order']
    raw_id_fields = ['photo']
    readonly_fields = ['get_preview']

    def get_preview(self, obj):
        return obj.photo.thumbnail_preview
    get_preview.short_description = 'Image preview'
    get_preview.allow_tags = True


class RouteItineraryInline(admin.TabularInline):
    model = RouteItinerary
    ordering = ['day_no']
    show_change_link = True


class RouteCabinInline(admin.TabularInline):
    model = RouteCabin
    ordering = ['order']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [RouteCarouselPhotoInline, RouteItineraryInline, RouteCabinInline]


class RouteItineraryPhotoInline(AdminImageMixin, admin.TabularInline):
    model = RouteItineraryPhoto
    ordering = ['order']
    raw_id_fields = ['photo']
    readonly_fields = ['get_preview']

    def get_preview(self, obj):
        return obj.photo.thumbnail_preview
    get_preview.short_description = 'Image preview'
    get_preview.allow_tags = True


class RouteItineraryPointInline(admin.TabularInline):
    model = RouteItineraryPoint
    ordering = ['order']


@admin.register(RouteItinerary)
class RouteItineraryAdmin(admin.ModelAdmin):
    inlines = [RouteItineraryPhotoInline, RouteItineraryPointInline]
