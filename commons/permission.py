from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        print('request', request)
        if request.user.is_superuser:
            return True
        return False
