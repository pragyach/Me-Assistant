from django.urls import path
from .views import list_meetings_and_notes

urlpatterns = [
    path('meetings/', list_meetings_and_notes, name='list_meetings_and_notes'),
]
