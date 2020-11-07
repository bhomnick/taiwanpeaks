from django.urls import path

from routes import views


urlpatterns = [
    path('', views.routes_list, name='routes-list'),
    path('detail', views.routes_detail_example, name='routes-detail-example'),
    path('<slug:slug>', views.routes_detail, name='routes-detail')
]
