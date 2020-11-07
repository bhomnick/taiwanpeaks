from django.urls import path

from routes import views


urlpatterns = [
    path('', views.routes_list, name='routes-list'),
    path('<slug:slug>', views.routes_detail, name='routes-detail')
]
