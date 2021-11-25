from django.conf.urls import url
from django.urls import path

from apps.events.views import EventListCreateAPIView, DrawingAPIView
from apps.home.views import home

urlpatterns = [
    url(r'^$', home, name='home'),
]