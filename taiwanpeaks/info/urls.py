from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path(
        'safety/permits',
        TemplateView.as_view(template_name='info/safety/permits.html'),
        name='info-safety-permits'
    ),
]
