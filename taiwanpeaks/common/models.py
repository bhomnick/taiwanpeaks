from django.db import models


class FeaturedRoute(models.Model):
    route = models.ForeignKey('routes.Route', on_delete=models.PROTECT)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return str(self.route)


class Location(models.Model):
    name = models.CharField(max_length=50)
    name_short = models.CharField(max_length=10)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

