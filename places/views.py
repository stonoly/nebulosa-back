from rest_framework import viewsets
from .models import Place
from .serializers import PlaceSerializer
from nebulosa_back.permissions import IsAuthenticated


class PlaceViewSet(viewsets.ModelViewSet):
    """
    This ViewSet handles all CRUD operations for Place:
    - list (GET)
    - retrieve (GET with ID)
    - create (POST)
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """ Autorize only some actions for the view """
        if self.action in ['list', 'retrieve', 'create']:
            return super().get_queryset()
        return Place.objects.none() 
    
