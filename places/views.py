from rest_framework import generics
from .models import Place
from .serializers import PlaceSerializer
from nebulosa_back.mixins import AdminPermissionMixin

class PlaceListView(AdminPermissionMixin, generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

class PlaceCreateView(generics.CreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer