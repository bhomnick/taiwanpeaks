from django.conf import settings
from django.shortcuts import render, get_object_or_404


from .models import Route


def routes_list(request):
    routes = Route.objects.filter(active=True)
    return render(request, 'routes/list.html', {
        'routes': routes
    })


def routes_detail(request, slug):
    route = get_object_or_404(Route, slug=slug)
    return render(request, 'routes/detail.html', {
        'route': route,
        'map_api_key': settings.THUNDERFOREST_API_KEY
    })
