from django.urls import path

from routes import views


urlpatterns = [
    path('', views.routes_list, name='routes-list'),
    path('detail', views.routes_detail, name='routes-detail')
]
