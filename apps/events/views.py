from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from apps.events.models import EventModel
from apps.events.serializers.event_serializers import EventSerializer, DrawingSerializer
from commons.pagination import PaginationAPIView
from commons.exceptions import ValidationError404


class EventListCreateAPIView(PaginationAPIView):
    queryset = EventModel.objects.select_related('client').prefetch_related('event_authorized').filter(is_deleted=False)
    serializer_class = EventSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS  # cool trick right? :)

    # We need to override get method to achieve pagination

    def get(self, request):
        serializer = ''
        page = self.paginate_queryset(self.queryset)
        type_event = self.request.query_params.get('type')
        keyword = self.request.query_params.get('keyword')
        if keyword is not None:
            page = page.filter(title__icontains=keyword)
        if type_event is not None:
            if type_event == '1' or type_event == '2':
                page = page.filter(type=type_event)
            elif type_event == '':
                page = page.filter(type__in=['1', '2'])
        if page is not None:
            serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        event = request.data
        serializer = EventSerializer(data=event)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(APIView):
    def get_detail(self, pk):
        try:
            return EventModel.objects.get(event_id=pk)
        except EventModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_detail(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        event = self.get_detail(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DrawingAPIView(APIView):

    def post(self, request, ticket_id, format=None):
        serializer = DrawingSerializer(data=request.data, context={"ticket_id": ticket_id, 'user': self.request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDeleteAPIView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            event = EventModel.objects.get(id=pk)
            return event
        except EventModel.DoesNotExist:
            raise ValidationError404()

    # We need to override get method to achieve pagination
    def post(self, request, pk):
        event = self.get_object(pk)
        event.is_deleted = True
        event.save()
        return Response(status=status.HTTP_200_OK)
