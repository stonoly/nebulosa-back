from django.urls import path
from .views import UserProfilListView

urlpatterns = [
    path('users/', UserProfilListView.as_view(), name='user-list'),
]