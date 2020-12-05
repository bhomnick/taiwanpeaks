from django.db import models

from common import constants


class Peak(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    name_zh = models.CharField(max_length=255, verbose_name='Name (中文)', help_text=(
        "This peak's Chinese name, i.e. 南湖大山"))
    height = models.IntegerField(help_text="Height in meters")
    latitude = models.DecimalField(max_digits=8, decimal_places=5, help_text="Positive number, 5 decimal places")
    longitude = models.DecimalField(max_digits=8, decimal_places=5, help_text="Positive number, 5 decimal places")
    rank = models.IntegerField(help_text="Peak rank from 1-100")
    difficulty = models.CharField(max_length=50, choices=constants.DIFFICULTY_CHOICES, help_text=(
        "A = beginner<br>B = intermediate<br>C = advanced<br>C+ = expert"
    ))
    list_photo = models.ForeignKey('photos.Photo', related_name='list_peaks', on_delete=models.PROTECT,
        help_text="Choose a good photo that's representative of this peak")
    locations = models.ManyToManyField('common.Location', help_text=(
        "Select any locations this peak falls in or borders. Most peaks have more than one."))
    national_park = models.CharField(max_length=50, choices=constants.NP_CHOICES, null=True, blank=True,
        help_text="If this peak is in a national park, select it here")

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return self.name

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

        return tags
