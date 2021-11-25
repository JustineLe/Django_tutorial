from django.shortcuts import render

from apps.home.querys import get_event_data


def home(request):
    events = get_event_data()
    return render(request, 'home/index.html', {
        'events': events,
    })
