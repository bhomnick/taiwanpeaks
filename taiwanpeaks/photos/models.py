import os
import uuid
from urllib.parse import urlparse
from urllib.request import urlopen

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.utils.functional import cached_property
from django.utils.html import format_html

import flickr_api
from model_utils import Choices
from model_utils.models import TimeStampedModel
from sorl.thumbnail import ImageField, get_thumbnail
from taggit.managers import TaggableManager


flickr_api.set_keys(api_key=settings.FLICKR_KEY, api_secret=settings.FLICKR_SECRET)


ATTR_LICENSE_CHOICES = Choices(
    ('cc0', 'CC0'),
    ('pdm', 'PDM'),
    ('cc_by', 'CC BY'),
    ('cc_by_sa', 'CC BY-SA'),
    ('cc_by_nc', 'CC BY-NC'),
    ('cc_by_nd', 'CC BY-ND'),
    ('cc_by_nc_sa', 'CC BY-NC-SA'),
    ('cc_by_nc_nd', 'CC BY-NC-ND')
)
ATTR_VERSION_CHOICES = Choices(
    '1.0',
    '2.0',
    '2.5',
    '3.0',
    '4.0'
)


class FlickrUpdater:
    licenses = {
        '1': ('cc_by_nc_sa', '2.0'),
        '2': ('cc_by_nc', '2.0'),
        '3': ('cc_by_nc_nd', '2.0'),
        '4': ('cc_by', '2.0'),
        '5': ('cc_by_sa', '2.0'),
        '6': ('cc_by_nd', '2.0'),
        '9': ('cc0', '1.0'),
        '10': ('pdm', '1.0')
    }

    @cached_property
    def flickr_photo(self):
        if not self.photo.flickr_id:
            raise ValueError('Photo is missing flickr_id.')
        return flickr_api.Photo(id=self.photo.flickr_id)

    def __init__(self, photo):
        self.photo = photo

    def update_all(self):
        self.set_image()
        self.set_license()

    def set_image(self):
        sizes = self.flickr_photo.getSizes()
        if 'Large 2048' not in sizes:
            raise ValueError('Photo does not have a "Large 2048" size avaialble.')
        url = sizes['Large 2048']['source']

        name = urlparse(url).path.split('/')[-1]
        content = ContentFile(urlopen(url).read())
        self.photo.image.save(name, content, save=True)

    def set_license(self):
        info = self.flickr_photo.getInfo()
        if info['license'] not in self.licenses:
            raise ValueError(f"Unknown licesnse: {license}")
        attr_license, attr_version = self.licenses[info['license']]

        self.photo.attr_author = info['owner'].username
        self.photo.attr_title = info['title']
        self.photo.attr_link = f"https://www.flickr.com/photos/{info['owner'].id}/{info['id']}/"
        self.photo.attr_license = attr_license
        self.photo.attr_version = attr_version

        self.photo.save()


def uuid_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('photos', filename)


class Photo(TimeStampedModel):
    image = ImageField(upload_to=uuid_photo_path, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    flickr_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    attr_author = models.CharField(max_length=255, null=True, blank=True)
    attr_title = models.CharField(max_length=255, null=True, blank=True)
    attr_link = models.URLField(null=True, blank=True)
    attr_license = models.CharField(max_length=50, choices=ATTR_LICENSE_CHOICES, null=True, blank=True)
    attr_version = models.CharField(max_length=5, choices=ATTR_VERSION_CHOICES, null=True, blank=True)

    tags = TaggableManager(blank=True)

    @property
    def thumbnail_preview(self):
        try:
            thumbnail = get_thumbnail(
                self.image,
                '200x200',
                upscale=False,
                quality=100
            )
            return format_html('<img src="{}" width="{}" height="{}">'.format(
                thumbnail.url,
                thumbnail.width,
                thumbnail.height
            ))
        except TypeError:
            return None

    def __str__(self):
        if self.attr_title:
            return self.attr_title
        return "No title"

    def update_from_flickr(self):
        FlickrUpdater(self).update_all()
