from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Tag, PlaceTag
from .serializers import TagSerializer, PlaceTagSerializer, TagSearchResponseSerializer
from nebulosa_back.permissions import IsAuthenticated
from .services import TagSearchService


class TagViewSet(viewsets.ModelViewSet):
    """
    This ViewSet handles all CRUD operations for Tag:
    - search_similar_tags (POST)
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """ Autorize only some actions for the view """
        if self.action in ['search_similar_tags']:
            return super().get_queryset()
        return Tag.objects.none()
    
    @action(detail=False, methods=['post'])
    def search_similar_tags(self, request):
        """
        Search for tags similar to a keyword.
        
        Args:
            request: The HTTP request containing the keyword to search for in request.data['name']
            
        Returns:
            Response: A JSON dictionary containing the tags sorted by decreasing similarity
            Format: {'tags': {'tag1': score1, 'tag2': score2, ...}}
            where score is a number between 0 and 1 (1 = identical, 0 = completely different)
        """
        search_keyword = request.data.get('name')
        if not search_keyword:
            return Response(
                {'error': 'The parameter "name" is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        search_service = TagSearchService()
        results = search_service.search_similar_tags(search_keyword)
        
        serializer = TagSearchResponseSerializer(data={'tags': results})
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)