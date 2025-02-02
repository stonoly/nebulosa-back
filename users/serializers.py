from nebulosa_back.core import BaseModelSerializer
from .models import UserProfile
from django.contrib.auth.models import User


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserProfileSerializer(BaseModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'birth_date']

    def to_representation(self, instance):

        dict = super().to_representation(instance)
        flatten_dict = self.flatten_data(dict, 'user') 
        return flatten_dict
