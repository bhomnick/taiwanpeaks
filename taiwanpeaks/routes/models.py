import os
import uuid

from django.db import models

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
    name_zh = models.CharField(max_length=255)
    description = models.TextField()
    capacity_beds = models.IntegerField(null=True, blank=True)
    capacity_tents = models.IntegerField(null=True, blank=True)
    altitude = models.IntegerField()
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=8, decimal_places=5)
    photo = models.ForeignKey('photos.Photo', related_name='cabins', on_delete=models.PROTECT)
    booking_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


def route_gpx_path(instance, filename):
    filename = f'{instance.slug}-{uuid.uuid4()}.gpx'
    return os.path.join('gpx', filename)


class Route(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    name_zh = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    intro = models.TextField()
    difficulty = models.CharField(max_length=50, choices=constants.DIFFICULTY_CHOICES)
    total_distance = models.IntegerField( )
    days_required = models.IntegerField()
    peak_count = models.IntegerField()
    locations = models.ManyToManyField('common.Location')
    public_transport_accessible = models.BooleanField()
    cabin_status = models.CharField(max_length=50, choices=CABIN_STATUS_CHOICES)
    header_background_photo = models.ForeignKey('photos.Photo', on_delete=models.PROTECT, related_name='header_background_routes')
    summary_background_photo = models.ForeignKey('photos.Photo', on_delete=models.PROTECT, related_name='summary_background_routes')
    gpx = models.FileField(upload_to=route_gpx_path, null=True, blank=True)
    np_permit_required = models.CharField(max_length=50, choices=constants.NP_CHOICES, null=True, blank=True)
    police_permit_required = models.BooleanField()
    custom_permit_info = models.TextField(null=True, blank=True)
    transportation_desc = models.TextField(null=True, blank=True)
    transportation_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def location_list_short(self):
        return [l.name_short for l in self.locations.all()]


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

    def __str__(self):
        return f'{str(self.route)} - Day {self.day_no}'


class RouteItineraryPoint(models.Model):
    route_itinerary = models.ForeignKey('RouteItinerary', on_delete=models.PROTECT, related_name='points')
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=ROUTE_POINT_CHOICES, null=True, blank=True)
    order = models.IntegerField()


class RouteItineraryPhoto(models.Model):
    route_itinerary = models.ForeignKey('RouteItinerary', on_delete=models.PROTECT, related_name='photos')
    photo = models.ForeignKey('photos.Photo', on_delete=models.PROTECT, related_name='route_itineraries')
    order = models.IntegerField()


class RouteCabin(models.Model):
    route = models.ForeignKey('Route', on_delete=models.PROTECT, related_name='cabins')
    cabin = models.ForeignKey('Cabin', on_delete=models.PROTECT, related_name='routes')
    order = models.IntegerField()


class RouteCarouselPhoto(models.Model):
    route = models.ForeignKey('Route', on_delete=models.PROTECT, related_name='carousel_photos')
    photo = models.ForeignKey('photos.Photo', on_delete=models.PROTECT, related_name='routes')
    order = models.IntegerField()

    class Meta:
        unique_together = ['route', 'photo']
