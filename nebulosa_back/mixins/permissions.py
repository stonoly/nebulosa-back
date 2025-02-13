from rest_framework.permissions import IsAuthenticated
from nebulosa_back.permissions import IsAdminUser, IsOwnerUser, IsAuthenticated

class AdminPermissionMixin:
    permission_classes = [IsAuthenticated, IsAdminUser]

class OwnerPermissionMixin:
    permission_classes = [IsAuthenticated, IsOwnerUser]

class AuthenticatedOrReadOnlyMixin:
    permission_classes = [IsAuthenticated]