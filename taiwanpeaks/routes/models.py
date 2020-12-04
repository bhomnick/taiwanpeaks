import os
import uuid

from django.db import models
from django.urls import reverse

from model_utils import Choices
from model_utils.models import TimeStampedModel

from common import constants


CABIN_STATUS_CHOICES = Choices(
    ('none', 'No cabins'),
    ('mixed', 'Mixed cabins/camping'),
    ('full', 'All cabins')
)
ROUTE_POINT_CHOICES = Choices(
    ('trailhead', 'Trailhead'),
    ('peak', 'Top 100 peak'),
    ('cabin', 'Cabin')
)
ITINERARY_REST_CHOICES = Choices(
    ('cabin', 'Cabin'),
    ('campground', 'Campground')
)


class Cabin(TimeStampedModel):
    name = models.CharField(max_length=255)
    name_zh = models.CharField(max_length=255, verbose_name='Name (中文)', help_text=(
        "Cabin's Chinese name, i.e. 南湖山屋"))
    description = models.TextField(help_text="A description of cabin amenities, water supply, and any special features. Approximately 250-300 characters")
    capacity_beds = models.IntegerField(null=True, blank=True, help_text="Number of bed slots available")
    capacity_tents = models.IntegerField(null=True, blank=True, help_text="Number of camp sites available")
    altitude = models.IntegerField(help_text="Altitude in meters")
    latitude = models.DecimalField(max_digits=8, decimal_places=5, help_text="Positive number, 5 decimal places")
    longitude = models.DecimalField(max_digits=8, decimal_places=5, help_text="Positive number, 5 decimal places")
    photo = models.ForeignKey('photos.Photo', related_name='cabins', on_delete=models.PROTECT)
    booking_link = models.URLField(null=True, blank=True, help_text=(
        "Booking URL if cabin is booked separately from permits, for instance Jiaminghu. "
        "Leave blank if cabin is booked along with permits."
    ))

    def __str__(self):
        return self.name


def route_gpx_path(instance, filename):
    filename = f'{instance.slug}-{uuid.uuid4()}.gpx'
    return os.path.join('gpx', filename)


class Route(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    name_zh = models.CharField(max_length=255, verbose_name='Name (中文)', help_text=(
        "Route name in Chinese, i.e. 北一段"))
    active = models.BooleanField(default=False, help_text=(
        "Check to publish for all users. If unchecked only staff users may preview "
        "this route."
    ))
    header_background_photo = models.ForeignKey('photos.Photo', on_delete=models.PROTECT, related_name='header_background_routes',
        help_text="Photo will appear behind route name/header.")
    intro = models.TextField(help_text="Short intro describing the highlights of this route. Approximately 400-500 characters.")
    difficulty = models.CharField(max_length=50, choices=constants.DIFFICULTY_CHOICES, help_text=(
        "Beginner = tourist-friendly (think Jade)<br>"
        "Intermediate = doable with some experience (think Nanhu)<br>"
        "Advanced = for experienced hikers (think central sections)<br>"
        "Expert = the 4 hurdles (S3, Mabo, Qilai East, Ganzhuowan)<br>"
        "If unsure ask for opinions."
    ))
    total_distance = models.IntegerField(help_text="Total route distance in km.")
    days_required = models.IntegerField()
    peak_count = models.IntegerField(help_text="Total number of top 100 peaks covered by this route.")
    locations = models.ManyToManyField('common.Location', help_text=(
        "Select any locations this route crosses. Many routes cross more than one."))
    public_transport_accessible = models.BooleanField(help_text=(
        "Check is trailheads are accessible via public transport."))
    cabin_status = models.CharField(null=True, blank=True, max_length=50, choices=CABIN_STATUS_CHOICES, help_text=(
        "All cabins = cabins available every night<br>"
        "Mixed cabins/camping = cabins available some nights<br>"
        "No cabins = no cabins available, must camp every night"
    ))
    summary_background_photo = models.ForeignKey('photos.Photo', on_delete=models.PROTECT, related_name='summary_background_routes',
        help_text="Photo will appear behind route summary section.")
    list_description = models.TextField(null=True, blank=True, help_text=(
        "Short route description used in the routes list view. No more than 120 characters."
    ))
    gpx = models.FileField(upload_to=route_gpx_path, null=True, blank=True)
    np_permit_required = models.CharField(max_length=50, choices=constants.NP_CHOICES, null=True, blank=True,
        verbose_name="National Park Permit Required", help_text="Select the appropriate park if a national park entry permit is required.")
    police_permit_required = models.BooleanField(help_text="Check if police mountain entry permit required.")
    custom_permit_info = models.TextField(null=True, blank=True, help_text=(
        "Used to override the default permit explanations if special circumstances "
        "apply to this route. Leave blank if only regular police/np permits required."
    ))
    transportation_desc = models.TextField(null=True, blank=True, verbose_name="Transportation description", help_text=(
        "Describe how to get to the trailhead, any public transportation options, "
        "the parking situation, etc."
    ))
    transportation_link = models.URLField(null=True, blank=True, help_text=(
        "An optional link to bus schedule or other external transportation resource."))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('routes-detail', args=[self.slug])

    @property
    def location_list_short(self):
        return [l.name_short for l in self.locations.all()]

    @property
    def difficulty_index(self):
        return constants.DIFFICULTY_CHOICES.index_of(self.difficulty)

    @property
    def filter_tags(self):
        # Level
        tags = [f'filter-level-{self.difficulty}']

        # Duration
        if self.days_required == 1:
            days = '1'
        elif self.days_required <= 3:
            days = '2to3'
        elif self.days_required <= 6:
            days = '4to6'
        else:
            days = '7plus'
        tags.append(f'filter-duration-{days}')

        # Public transport
        if self.public_transport_accessible:
            tags.append('filter-publictransport-yes')

        # Cabins
        if self.cabin_status:
            tags.append(f'filter-cabins-{self.cabin_status}')

        return tags


class RouteItinerary(models.Model):
    route = models.ForeignKey('Route', related_name='itineraries', on_delete=models.PROTECT)
    day_no = models.IntegerField()
    total_distance = models.DecimalField(max_digits=3, decimal_places=1)
    total_hours = models.DecimalField(max_digits=3, decimal_places=1)
    rest_name = models.CharField(max_length=255, null=True, blank=True)
    rest_type = models.CharField(max_length=50, choices=ITINERARY_REST_CHOICES, null=True, blank=True)
    water_desc = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['day_no']
        verbose_name = "Route day itinerary"
        verbose_name_plural = "Route day itineraries"

    def __str__(self):
        return ''


class RouteItineraryPoint(models.Model):
    route_itinerary = models.ForeignKey('RouteItinerary', on_delete=models.PROTECT, related_name='points')
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=ROUTE_POINT_CHOICES, null=True, blank=True)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']


class RouteItineraryPhoto(models.Model):
    route_itinerary = models.ForeignKey('RouteItinerary', on_delete=models.PROTECT, related_name='photos')
    photo = models.ForeignKey('photos.Photo', on_delete=models.PROTECT, related_name='route_itineraries')
    order = models.IntegerField()

    class Meta:
        ordering = ['order']


class RouteCabin(models.Model):
    route = models.ForeignKey('Route', on_delete=models.PROTECT, related_name='cabins')
    cabin = models.ForeignKey('Cabin', on_delete=models.PROTECT, related_name='routes')
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return ''


class RouteCarouselPhoto(models.Model):
    route = models.ForeignKey('Route', on_delete=models.PROTECT, related_name='carousel_photos')
    photo = models.ForeignKey('photos.Photo', on_delete=models.PROTECT, related_name='routes')
    order = models.IntegerField()

    class Meta:
        unique_together = ['route', 'photo']
        ordering = ['order']

    def __str__(self):
        return ''


class RoutePeak(models.Model):
    route = models.ForeignKey('Route', on_delete=models.PROTECT, related_name='route_peaks')
    peak = models.ForeignKey('peaks.Peak', on_delete=models.PROTECT, related_name='routes')
    order = models.IntegerField()

    class Meta:
        unique_together = ['route', 'peak']
        ordering = ['order']

    def __str__(self):
        return ''
