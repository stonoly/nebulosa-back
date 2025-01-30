from rest_framework import generics
from .models import Place
from .serializers import PlaceSerializer

class PlaceListView(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

class PlaceCreateView(generics.CreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer