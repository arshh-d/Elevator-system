from .models import Elevator, ElevatorSystem

def create_elevators(system_name, system_id: int, max_floor, count: int):
    
    new_system, created = ElevatorSystem.objects.get_or_create(
        elevator_system_id=system_id,
        name=system_name,
        max_floor=max_floor,
        elevator_count=count)
    new_system.save()

    for i in range(count):
        new_elevator = Elevator.objects.create(elevator_system_id = new_system, elevator_id = i+1)
        new_elevator.save()
