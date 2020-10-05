from django.shortcuts import render, get_object_or_404

from .models import Route


def routes_list(request):
    return render(request, 'routes/list.html')


def routes_detail(request, slug):
    route = get_object_or_404(Route, slug=slug)
    return render(request, 'routes/detail.html', {
        'route': route
    })


def routes_detail_example(request):
    return render(request, 'routes/detail_example.html')
