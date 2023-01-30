from django.urls import path
from .views import (create_elevator_system, get_all_elevators,
    get_elevator, create_request, update_elevator_status)

urlpatterns = [
    path('create/', create_elevator_system, name="create_elevator_system"),
    path('get_system/<int:system_id>/',
         get_all_elevators, name="get_all_elevators"),
    path('get_elevator/<int:system_id>/<int:elevator_id>/',
         get_elevator, name="get_elevator"),
    path('create_request/', create_request, name="create_request"),
    path('update_status', update_elevator_status, name='update_status')
]
