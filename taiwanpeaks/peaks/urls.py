from django.urls import path

from . import views


urlpatterns = [
    path('', views.peaks_list, name='peaks-list'),
    path('<slug:slug>', views.peaks_detail, name='peaks-detail')
]
