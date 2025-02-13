from .authenticated import IsAuthenticated

class IsOwnerUser(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and obj.user == request.user