from rest_framework import serializers
from .models import Place, PlaceAdress

class PlaceAdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceAdress
        fields = ['number', 'street', 'city', 'state', 'country', 'zip_code', 'latitude', 'longitude']

class PlaceSerializer(serializers.ModelSerializer):
    address = PlaceAdressSerializer()

    class Meta:
        model = Place
        fields = ['name', 'description', 'address', 'created_at', 'updated_at']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = PlaceAdress.objects.create(**address_data)
        place = Place.objects.create(address=address, **validated_data)
        return place
