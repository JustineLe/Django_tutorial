from rest_framework import serializers, status
import datetime
from apps.events.models import EventModel, DrawingModel, TicketModel
from commons.exceptions import ValidationError, ValidationError404


class EventSerializer(serializers.ModelSerializer):
    is_locked = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = EventModel
        fields = ['id', 'title', 'is_locked', 'image_url']

    # custom response trả về cho field is_locked
    def get_is_locked(self, obj):
        is_locked = 0
        if obj.is_private and len(obj.event_authorized.all()) == 0:
            is_locked = 1

        return is_locked

    # custom response trả về cho field image_url
    def get_image_url(self, obj):
        # image_path = obj.image_path.first()
        image_path = obj.image_path.all()  # get all dữ liệu image path theo event
        image_path_list = list(image_path)
        if len(image_path_list) > 0:
            image_path = image_path_list[0]
            return image_path.image_url
        return ''


class DrawingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawingModel
        fields = ['ticket_id', 'is_elected', 'is_purchased']

        extra_kwargs = {
            'is_elected': {'read_only': True},
            # 'name': {'read_only': True},
            # 'start_datetime': {'read_only': True},
            # 'end_datetime': {'read_only': True},
            # 'price': {'read_only': True},
            # 'quantity': {'read_only': True},
            # 'total_price': {'read_only': True},
        }

    def validate(self, attrs):
        context = self.context
        if 'ticket_id' in context:
            ticket_id = context['ticket_id']
            user = context['user']
            now = datetime.datetime.now()
            try:
                TicketModel.objects.get(ticket_id=ticket_id, performance__event__client_id=user.client_id,
                                        performance__ticket_available_flag=True, drawing_flag=True,
                                        drawing_application_deadline__gt=now, drawing_status=False)
            except TicketModel.DoesNotExist:
                raise ValidationError404(code='TICKET_DOSE_NOT_EXIST', detail='không có ticket')
        else:
            raise ValidationError404(code='TICKET_DOSE_NOT_EXIST', detail='không có ticket')
        return attrs

    def save(self, **kwargs):
        context = self.context
        ticket_id = context['ticket_id']
        user = context['user']

        drawing = DrawingModel()
        drawing.ticket_id = ticket_id
        drawing.user_id = user.id
        drawing.is_elected = False
        drawing.is_purchased = False
        drawing.save()
        return drawing


class TicketSerializer(serializers.ModelSerializer):
    is_archived = serializers.SerializerMethodField()
    ticket_available_flag = serializers.SerializerMethodField()

    class Meta:
        model = TicketModel
        fields = ['ticket_id', 'ticket_available_flag', 'is_archived', 'drawing_flag', 'drawing_application_deadline',
                  'drawing_status']

    def get_is_archived(self, obj):
        is_archive = obj.performance_id.event_id.is_archived
        if is_archive is not None:
            return is_archive
        else:
            return 0

    def get_ticket_available_flag(self, obj):
        ticket_available_flag = obj.performance_id.ticket_availableL_flag
        if ticket_available_flag is not None:
            return ticket_available_flag
        else:
            return 0


class PerformancesSerializer(serializers.ModelSerializer):
    start_datetime = serializers.SerializerMethodField()
    end_datetime = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = TicketModel
        fields = ['ticket_id', 'name', 'start_datetime', 'end_datetime', 'price', 'quantity', 'total_price']

    def get_start_datetime(self, obj):
        start_datetime = obj.performance_id.start_datetime
        if start_datetime is not None:
            return start_datetime
        else:
            return ""

    def get_end_datetime(self, obj):
        end_datetime = obj.performance_id.end_datetime
        if end_datetime is not None:
            return end_datetime
        else:
            return ""

    def get_quantity(self):
        return 1

    def get_total_price(self, obj):
        total_price = obj.price
        if total_price is not None:
            return total_price
        else:
            return ""
