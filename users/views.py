from rest_framework import generics
from .models import UserProfile
from .serializers import UserProfileSerializer
from nebulosa_back.permissions import IsOwnerUser, IsAuthenticated

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    This ViewSet handles all CRUD operations for UserProfile:
    - list (GET)
    - retrieve (GET with ID)
    - create (POST)
    - update (PUT / PATCH)
    - destroy (DELETE)
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
    
