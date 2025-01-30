from django.urls import path
from .views import PlaceListView, PlaceCreateView

urlpatterns = [
    path('places/', PlaceListView.as_view(), name='place-list'),
    path('places/create/', PlaceCreateView.as_view(), name='place-create'),
]
