from django.db import models
from django.utils.html import format_html

from model_utils import Choices
from sorl.thumbnail import ImageField, get_thumbnail


ATTR_LICENSE_CHOICES = Choices(
    ('cc0', 'CC0 1.0'),
    ('pdm', 'PDM'),
    ('cc_by', 'CC BY 2.0'),
    ('cc_by_sa', 'CC BY-SA 2.0'),
    ('cc_by_nc', 'CC BY-NC 2.0'),
    ('cc_by_nd', 'CC BY-ND 2.0'),
    ('cc_by_nc_sa', 'CC BY-NC-SA 2.0'),
    ('cc_by_nc_nd', 'CC BY-NC-ND 2.0')
)


class Photo(models.Model):
    image = ImageField()
    attr_author = models.CharField(max_length=255, null=True, blank=True)
    attr_title = models.CharField(max_length=255, null=True, blank=True)
    attr_link = models.URLField(null=True, blank=True)
    attr_license = models.CharField(max_length=50, choices=ATTR_LICENSE_CHOICES, null=True, blank=True)

    @property
    def thumbnail_preview(self):
        thumbnail = get_thumbnail(
            self.image,
            '300x300',
            upscale=False,
            crop=False,
            quality=100
        )
        return format_html('<img src="{}" width="{}" height="{}">'.format(
            thumbnail.url,
            thumbnail.width,
            thumbnail.height
        ))

    def __str__(self):
        if self.attr_title:
            return self.attr_title
        return "No title"
