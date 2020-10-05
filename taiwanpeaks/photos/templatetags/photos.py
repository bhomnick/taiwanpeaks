from django import template


register = template.Library()


@register.inclusion_tag('photos/_components/attribution.html')
def attribution(photo):
    return {'photo': photo}
