from django import template

from ..models import Photo


register = template.Library()


@register.simple_tag
def slug_photo(slug):
    photo = Photo.objects.filter(slug=slug).first()
    if not photo:
        return Photo.objects.get(default_slug=True)
    return photo


@register.inclusion_tag('photos/_components/attribution.html')
def attribution(photo):
    return {'photo': photo}
