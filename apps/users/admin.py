from django import forms
from django.contrib import admin

from apps.users.models import UserAccountModel


class UserForm(forms.ModelForm):
    class Meta:
        model = UserAccountModel
        exclude = ["email", "anonymous", "line_id", "liff_id", "gender", "pregnant", "age", "height", "weight",
                   "created_at",
                   "updated_at", "last_login"]

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


@admin.register(UserAccountModel)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username']
    ordering = ['-created_at']
    search_fields = ['display_name', 'username']
    list_filter = ['username']

    # form = UserForm

    def get_queryset(self, request):
        qs = super(CustomUserAdmin, self).get_queryset(request)
        return qs.filter(is_staff=True)

    def username(self, obj):
        return obj.username

    username.short_description = 'Line ユーザー名'
