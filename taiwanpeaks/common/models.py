from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=50)
    name_short = models.CharField(max_length=10)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

