from django import forms
from django.contrib import admin

from apps.events.models import EventModel, ImagePathModel


class EventForm(forms.ModelForm):
    class Meta:
        model = EventModel
        # fields = ['is_deleted']
        exclude = ['is_deleted']

    def clean(self):
        cleaned_data = super().clean()

    def save(self, commit=True):
        # Save the provided password in hashed format
        event = super(EventForm, self).save(commit=False)

        if commit:
            event.save()
            image_path = ImagePathModel()
            image_path.event = event
            image_path.image_url = 'path_1'
            image_path.save()
        return event


class AudioInline(admin.StackedInline):
    readonly_fields = ['created_at']
    model = ImagePathModel
    extra = 0


@admin.register(EventModel)
class CustomEvent(admin.ModelAdmin):
    list_display = ['title', 'body', 'is_private_custom']  # Các field hiển thị trên danh sách list
    ordering = ['-created_at']  # thực hiện order theo
    search_fields = ['title', 'body']
    list_filter = ['is_private']
    # inlines = [AudioInline, ]

    form = EventForm

    # custom queryset để hiện thị data
    def get_queryset(self, request):
        qs = super(CustomEvent, self).get_queryset(request)
        return qs.filter(is_deleted=False)

    # custom hiển thị field private
    def is_private_custom(self, obj):
        return '1' if obj.is_private else '0'

    is_private_custom.short_description = 'Private'
    # def username(self, obj):
    #     return obj.username

    # username.short_description = 'Line ユーザー名'
