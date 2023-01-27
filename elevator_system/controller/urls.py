from django.urls import path
from .views import create_elevator_system, get_all_elevators, get_elevator

urlpatterns = [
    path('create/', create_elevator_system, name="create_elevator_system"),
    path('get_system/<int:system_id>/', get_all_elevators, name="get_all_elevators"),
    path('get_elevator/<int:system_id>/<int:elevator_id>/', get_elevator, name="get_elevator")
]