from django.shortcuts import render

from .models import FeaturedRoute


def homepage(request):
    return render(request, 'homepage.html', {
        'featured_routes': FeaturedRoute.objects.all()
    })
