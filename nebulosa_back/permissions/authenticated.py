from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, User) and request.user.is_authenticated