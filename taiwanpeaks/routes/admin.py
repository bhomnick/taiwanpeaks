from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from sorl.thumbnail.admin import AdminImageMixin

from .models import Route, RouteCarouselPhoto, RouteItinerary, \
    RouteItineraryPhoto, RouteItineraryPoint, RouteCabin, Cabin, \
    RoutePeak


@admin.register(Cabin)
class CabinAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ['name', 'name_zh', 'get_preview']
    search_fields = ['name', 'name_zh']
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
    extra = 0
    verbose_name = "carousel photo"
    verbose_name_plural = "carousel photos"

    def get_preview(self, obj):
        return obj.photo.thumbnail_preview
    get_preview.short_description = 'Image preview'
    get_preview.allow_tags = True


class RouteItineraryInline(admin.TabularInline):
    model = RouteItinerary
    template = "admin/_components/itinerary_inline.html"
    ordering = ['day_no']
    fields = ['day_no', 'total_distance', 'total_hours', 'title', 'edit_link']
    readonly_fields = fields
    verbose_name_plural = "itinerary"
    can_delete = False
    extra = 0
    max_num = 0

    def edit_link(self, obj):
        url = reverse('admin:routes_routeitinerary_change', args=[obj.pk])
        return format_html(f'<a target="_blank" href="{url}">Details/Edit</a>')
    edit_link.allow_tags = True


class RouteCabinInline(admin.TabularInline):
    model = RouteCabin
    verbose_name = "cabin"
    verbose_name_plural = "cabins"
    extra = 0
    ordering = ['order']


class RoutePeakInline(admin.TabularInline):
    model = RoutePeak
    verbose_name = "peak"
    verbose_name_plural = "peaks"
    extra = 0
    ordering = ['order']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['header_background_photo', 'summary_background_photo']
    inlines = [RouteCarouselPhotoInline, RouteItineraryInline, RouteCabinInline,
               RoutePeakInline]
    filter_horizontal = ['locations']
    fieldsets = (
        ('Visibility', {
            'fields': ['active']
        }),
        ('Header', {
            'fields': ['name', 'slug', 'name_zh', 'header_background_photo']
        }),
        ('Basic Details', {
            'fields': ['intro', 'difficulty', 'total_distance', 'days_required',
                       'peak_count', 'locations', 'public_transport_accessible',
                       'cabin_status']
        }),
        ('Summary', {
            'fields': ['summary_background_photo']
        }),
        ('List View', {
            'fields': ['list_description']
        }),
        ('Map', {
            'fields': ['gpx']
        }),
        ('Permits', {
            'fields': ['np_permit_required', 'police_permit_required', 'custom_permit_info']
        }),
        ('Transportation', {
            'fields': ['transportation_desc', 'transportation_link']
        })
    )


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
