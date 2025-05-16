from rest_framework import serializers
from .models import Tag, PlaceTag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'created_at', 'updated_at', 'creator']

class PlaceTagSerializer(serializers.ModelSerializer):
    tag_name = serializers.CharField(source='tag.name', read_only=True)
    place_name = serializers.CharField(source='place.name', read_only=True)

    class Meta:
        model = PlaceTag
        fields = ['id', 'tag', 'tag_name', 'place', 'place_name', 'description', 
                 'grade', 'created_at', 'updated_at', 'creator']

class TagSearchResponseSerializer(serializers.Serializer):
    tags = serializers.DictField(
        child=serializers.FloatField(),
        help_text="Dictionary of tag names and their similarity scores"
    )