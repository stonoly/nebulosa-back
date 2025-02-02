from rest_framework import generics
from .models import UserProfile
from .serializers import UserProfileSerializer
from nebulosa_back.mixins import AuthenticatedOrReadOnlyMixin

class UserProfilListView(AuthenticatedOrReadOnlyMixin, generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer