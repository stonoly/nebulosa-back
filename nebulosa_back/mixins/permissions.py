from rest_framework.permissions import IsAuthenticated
from nebulosa_back.permissions import IsAdminUser, IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly

class AdminPermissionMixin:
    permission_classes = [IsAuthenticated, IsAdminUser]

class OwnerPermissionMixin:
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

class AuthenticatedOrReadOnlyMixin:
    permission_classes = [IsAuthenticatedOrReadOnly]