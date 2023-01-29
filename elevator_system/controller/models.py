from django.db import models

class ElevatorSystem(models.Model):
    elevator_system_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)
    max_floor = models.IntegerField()
    elevator_count = models.IntegerField()


class Elevator(models.Model):

    class CurrentStatus(models.IntegerChoices):
        UP = 1
        HALT = 0
        DOWN = -1
    
    elevator_system_id = models.ForeignKey(ElevatorSystem, on_delete=models.CASCADE)
    elevator_id = models.IntegerField()
    on_floor = models.IntegerField(default=0)
    working = models.BooleanField(default=True)
    status = models.IntegerField(choices=CurrentStatus.choices,default=CurrentStatus.HALT)
    door_open = models.BooleanField(default=False)


class ElevatorRequest(models.Model):

    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    elevator_system = models.ForeignKey(ElevatorSystem, on_delete=models.CASCADE)
    requested_floor = models.PositiveSmallIntegerField()
    destination_floor = models.PositiveSmallIntegerField()
    request_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)