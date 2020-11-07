from django.conf import settings
from django.shortcuts import render, get_object_or_404


from .models import Peak


def peaks_list(request):
    peaks = Peak.objects.all()
    return render(request, 'peaks/list.html', {
        'peaks': peaks
    })


def peaks_detail(request, slug):
    peak = get_object_or_404(Peak, slug=slug)
    return render(request, 'peaks/detail.html', {
        'peak': peak,
        'map_api_key': settings.THUNDERFOREST_API_KEY
    })
