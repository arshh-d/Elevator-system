from .models import Elevator, ElevatorSystem, ElevatorRequest
from threading import Thread


def create_elevators(system_name, system_id: int, max_floor, count: int):

    new_system, created = ElevatorSystem.objects.get_or_create(
        elevator_system_id=system_id,
        name=system_name,
        max_floor=max_floor,
        elevator_count=count)
    new_system.save()

    for i in range(count):
        new_elevator = Elevator.objects.create(
            elevator_system_id=new_system, elevator_id=i+1)
        new_elevator.save()


class RunThread(Thread):
    '''
    A different thread running in an infinite loop
    to process all the requests made to an elevator
    '''

    def run(self):
        while True:
            final_run()


def move_to_floor(floor_number, elevator_object):
    if floor_number > elevator_object.on_floor:
        # Start going up
        elevator_object.status = 1
    elif floor_number < elevator_object.on_floor:
        # Start going down
        elevator_object.status = -1
    elevator_object.on_floor = floor_number
    elevator_object.status = 0
    elevator_object.save()


def get_nearest_elevator(elevator_system, request_start):
    elevators_working = Elevator.objects.filter(
            elevator_system_id=elevator_system.elevator_system_id,
            working=True)
    elevator_object = None
    min_distance = elevator_system.max_floor
    for elevator in elevators_working:
        if abs(elevator.on_floor - request_start) < min_distance:
            min_distance = elevator.on_floor - request_start
            elevator_object = elevator
    return elevator_object

def process_request(elevator_system: ElevatorSystem):

    requests_pending = ElevatorRequest.objects.filter(
        elevator_system=elevator_system,
        is_active=True,
    ).order_by('request_time')

    for elev_request in requests_pending:
        request_start = elev_request.requested_floor
        request_destination = elev_request.destination_floor

        elevator_object = get_nearest_elevator(elevator_system, request_start)

        elev_request.elevator = elevator_object
        elev_request.save()

        # Invalid Cases, this can be taken care of using ModelManagers earlier
        # 1
        if (request_destination < 0
                or request_destination > elevator_system.max_floor
                or request_start < 0
                or request_start > elevator_system.max_floor
                or request_destination == request_start):
            elev_request.is_active = False
            elev_request.save()
            continue

        # Close the door
        elevator_object.door_open = False

        # move to elevator to the requested floor
        move_to_floor(request_start, elevator_object)
        elevator_object.door_open = True
        elevator_object.save()

        # Let people get in, Close the door
        elevator_object.door_open = False

        # move to elevator to destination floor
        move_to_floor(request_destination, elevator_object)
        elevator_object.door_open = True
        elevator_object.door_open = False
        elevator_object.save()

        elev_request.is_active = False
        elev_request.save()


def final_run():

    elevator_systems = ElevatorSystem.objects.all().order_by('elevator_system_id')

    try:
        for elevator_system in elevator_systems:
            process_request(elevator_system=elevator_system)
    except Exception as exc:
        print(exc)
