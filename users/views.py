from rest_framework import viewsets
from .models import UserProfile
from .serializers import UserProfileSerializer
from nebulosa_back.permissions import IsOwnerUser, IsAuthenticated


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    This ViewSet handles all CRUD operations for UserProfile:
    - list (GET)
    - retrieve (GET with ID)
    - create (POST)
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            return []
        if self.action in ['retrieve']:
            return [IsOwnerUser()]
        return super().get_permissions()
    
    def get_queryset(self):
        """ Autorize only some actions for the view """
        if self.action in ['list', 'retrieve', 'create']:
            return super().get_queryset()
        return UserProfile.objects.none() 
    
