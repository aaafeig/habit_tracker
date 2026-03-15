from django.urls import path
from .views import (
    HabitListCreateView,
    HabitRetrieveUpdateDestroyView,
    PublicHabitListView,
)

urlpatterns = [
    path("", HabitListCreateView.as_view()),
    path("<int:pk>/", HabitRetrieveUpdateDestroyView.as_view()),
    path("public/", PublicHabitListView.as_view()),
]
