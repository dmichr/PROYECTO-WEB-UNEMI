from django.urls import path
from .views import *

urlpatterns = [
    path('listado/', BoletinListView.as_view(), name='listado_boletines'),
    path('events.json', get_events, name='get_events'),
]