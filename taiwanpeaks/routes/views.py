from django.shortcuts import render


def routes_list(request):
    return render(request, 'routes/list.html')


def routes_detail(request):
    return render(request, 'routes/detail.html')
