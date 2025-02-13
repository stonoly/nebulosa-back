from nebulosa_back.core import BaseModelSerializer
from .models import UserProfile
from django.contrib.auth.models import User
from .services import UserService


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

    def to_representation(self, instance):
        """ Remove the password from the response """
        
        dict = super().to_representation(instance)
        dict.pop('password')
        return dict


class UserProfileSerializer(BaseModelSerializer):
    user = UserSerializer()

    def __init__(self, *args, **kwargs):
        """ Define the keys to flatten and unflatten the data """

        self._keys_to_nested = ['username', 'first_name', 'last_name', 'email', 'password']
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserProfile
        fields = ['user', 'birth_date']

    def to_representation(self, instance):
        """ Flatten the data user """

        dict = super().to_representation(instance)
        flatten_dict = self.flatten_data(dict, 'user') 
        return flatten_dict
    
    def to_internal_value(self, data):
        """ Unflatten the data user """

        data = self.unflatten_data(data, self._keys_to_nested, 'user')
        return super().to_internal_value(data)
    
    def create(self, validated_data):
        """ Use the service layer to create user and profile """

        user_data = validated_data.pop('user')
        user = UserService.create_user_with_profile(**user_data)
        
        user_profile = UserProfile.objects.get(user=user)
        user_profile.birth_date = validated_data.get('birth_date')
        user_profile.save()
        
        return user_profile
