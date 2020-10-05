from django.db import models

from model_utils import Choices

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


class Cabin(models.Model):
    name = models.CharField(max_length=255)
    name_zh = models.CharField(max_length=255)
    description = models.TextField()
    capacity = models.IntegerField()
    altitude = models.IntegerField()
    latitude = models.DecimalField(max_digits=8, decimal_places=4)
    longitude = models.DecimalField(max_digits=8, decimal_places=4)
    photo = models.ForeignKey('photos.Photo', related_name='cabins', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    name_zh = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    intro = models.TextField()
    difficulty = models.CharField(max_length=50, choices=constants.DIFFICULTY_CHOICES)
    total_distance = models.IntegerField( )
    days_required = models.IntegerField()
    peak_count = models.IntegerField()
    location = models.CharField(max_length=50, choices=constants.NP_CHOICES)
    public_transport_accessible = models.BooleanField()
    cabin_status = models.CharField(max_length=50, choices=CABIN_STATUS_CHOICES)
    header_background_photo = models.ForeignKey('photos.Photo', on_delete=models.PROTECT, related_name='header_background_routes')
    summary_background_photo = models.ForeignKey('photos.Photo', on_delete=models.PROTECT, related_name='summary_background_routes')
    np_permit_required = models.CharField(max_length=50)
    police_permit_required = models.BooleanField()
    transportation_desc = models.TextField()
    transportation_link = models.URLField()

    def __str__(self):
        return self.name


class RouteItinerary(models.Model):
    route = models.ForeignKey('Route', related_name='itineraries', on_delete=models.PROTECT)
    day_no = models.IntegerField()
    total_distance = models.DecimalField(max_digits=3, decimal_places=1)
    total_hours = models.DecimalField(max_digits=3, decimal_places=1)
    water_desc = models.CharField(max_length=255)

    def __str__(self):
        return f'{str(self.route)} - Day {self.day_no}'


class RouteItineraryPoint(models.Model):
    route_itinerary = models.ForeignKey('RouteItinerary', on_delete=models.PROTECT, related_name='points')
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=ROUTE_POINT_CHOICES)
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
