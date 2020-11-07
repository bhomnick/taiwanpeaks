from django.shortcuts import render

from .models import FeaturedPeak, FeaturedRoute


def homepage(request):
    return render(request, 'homepage.html', {
        'featured_peaks': FeaturedPeak.objects.all(),
        'featured_routes': FeaturedRoute.objects.all()
    })
