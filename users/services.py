from django.contrib.auth.models import User
from .models import UserProfile


class UserService:
    
    @staticmethod
    def create_user_with_profile(username, first_name, last_name, email, password):
        """ Create a User with data from the Request """

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=False,
            is_superuser=False
        )
        user.set_password(password) 
        user.save()

        return user