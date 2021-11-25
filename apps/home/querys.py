from apps.events.models import EventModel


def get_event_data():
    events = EventModel.objects.filter(is_deleted=False)
    return events