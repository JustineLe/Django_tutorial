from django.conf.urls import url
from django.urls import path
from apps.events.views import EventListCreateAPIView, EventDetail, DrawingAPIView, EventDeleteAPIView

urlpatterns = [
    url(r'^/events$', EventListCreateAPIView.as_view(), name='event_list'),
    url(r'^/events/<int:pk>$', EventDetail.as_view(), name='event_detail'),
    path('/event/<int:pk>', EventDeleteAPIView.as_view(), name='event_delete'),
    path('/tickets/<int:ticket_id>/drawings', DrawingAPIView.as_view(), name='drawings'),
]
