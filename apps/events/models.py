from django.db import models

from apps.users.models import ClientModel, UserAccountModel
from commons.models import BaseModel


class EventModel(BaseModel):
    client = models.ForeignKey(ClientModel, on_delete=models.CASCADE, null=True, related_name='events',
                               verbose_name='Khách hàng')
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='Tiêu đề')
    body = models.TextField(max_length=255, null=True, blank=True, verbose_name='Nội dung')
    is_private = models.BooleanField(default=False, choices=((0, 'No'), (1, 'Yes')))

    class Meta:
        db_table = 'events'
        verbose_name_plural = 'Sự kiện'


class EventAuthorizedModel(BaseModel):
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE, null=True, related_name='event_authorized')
    user = models.ForeignKey(UserAccountModel, on_delete=models.CASCADE, null=True, related_name='event_authorized')

    class Meta:
        db_table = 'event_authorized'


class ImagePathModel(BaseModel):
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE, null=True, related_name='image_path')
    user = models.ForeignKey(UserAccountModel, on_delete=models.CASCADE, null=True, related_name='image_path')
    image_url = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'image_path'


class PerformancesModel(BaseModel):
    choice_ticket_available_flag = (
        (0, 'Not available'),
        (1, 'Available')
    )
    performance_id = models.AutoField(primary_key=True)
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    streaming_method = models.IntegerField(null=True)
    name = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    capacity = models.IntegerField(null=True)
    ticket_available_flag = models.SmallIntegerField(choices=choice_ticket_available_flag)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'performances'


class TicketModel(BaseModel):
    ticket_id = models.AutoField(primary_key=True)
    performance = models.ForeignKey(PerformancesModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    points_required = models.IntegerField()
    expiration_datetime = models.DateTimeField()
    drawing_flag = models.BooleanField()
    drawing_application_deadline = models.DateTimeField(null=True)
    drawing_status = models.BooleanField()
    stamp_available_flag = models.BooleanField()
    max_number_of_tickets = models.IntegerField()
    number_of_issued_tickets = models.IntegerField()
    is_seat_id_assigned = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tickets'


class DrawingModel(BaseModel):
    ticket = models.ForeignKey(TicketModel, on_delete=models.CASCADE, )
    user = models.ForeignKey(UserAccountModel, on_delete=models.CASCADE)
    is_elected = models.BooleanField()
    is_purchased = models.BooleanField()

    class Meta:
        db_table = 'drawing'
