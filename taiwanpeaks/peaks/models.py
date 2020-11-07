from django.db import models

from common import constants


class Peak(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    name_zh = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    height = models.IntegerField()
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=8, decimal_places=5)
    rank = models.IntegerField()
    difficulty = models.CharField(max_length=50, choices=constants.DIFFICULTY_CHOICES)
    list_photo = models.ForeignKey('photos.Photo', related_name='list_peaks', on_delete=models.PROTECT)
    locations = models.ManyToManyField('common.Location')
    national_park = models.CharField(max_length=50, choices=constants.NP_CHOICES, null=True, blank=True)

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return self.name

    @property
    def difficulty_index(self):
        return constants.DIFFICULTY_CHOICES.index_of(self.difficulty)

    @property
    def filter_tags(self):
        # Level
        tags = [f'filter-level-{self.difficulty}']

        return tags
