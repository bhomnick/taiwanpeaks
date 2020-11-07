from django import template

from ..models import Photo


register = template.Library()


@register.simple_tag
def photo_by_tag(tag):
    photo = Photo.objects.filter(tags__name=tag).first()
    if not photo:
        return Photo.objects.filter(tags__name='default-by-tag').first()
    return photo


@register.inclusion_tag('photos/_components/attribution.html')
def attribution(photo):
    return {'photo': photo}
