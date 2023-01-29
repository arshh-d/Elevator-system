from django.contrib import admin
from .models import Elevator, ElevatorSystem, ElevatorRequest

admin.site.register(Elevator)
admin.site.register(ElevatorSystem)
admin.site.register(ElevatorRequest)