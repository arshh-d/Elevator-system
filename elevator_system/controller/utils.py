from .models import Elevator, ElevatorSystem, ElevatorRequest
from threading import Thread
from loguru import logger
import time


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
            time.sleep(4)


def move_to_floor(floor_number: int, elevator_object: Elevator):
    """moves elevator to given floor

    Args:
        floor_number (int): floor to move
        elevator_object (Elevator): elevator which will move
    """
    if floor_number > elevator_object.on_floor:
        elevator_object.status = 1
        logger.info(
            f"elevator: {elevator_object.elevator_system_id.name}:{elevator_object.elevator_id} moving UP")
    elif floor_number < elevator_object.on_floor:
        elevator_object.status = -1
        logger.info(
            f"elevator: {elevator_object.elevator_system_id.name}:{elevator_object.elevator_id} moving DOWN")
        # logger.log(
        #     f"elevator: {elevator_object.elevator_system_id.name}:{elevator_object.elevator_id} moving {elevator_object.status}")

    elevator_object.on_floor = floor_number
    logger.info(
        f"elevator: {elevator_object.elevator_system_id.name}:{elevator_object.elevator_id} reached on floor: {elevator_object.on_floor}")
    logger.info(
        f"elevator: {elevator_object.elevator_system_id.name}:{elevator_object.elevator_id} door opening")
    elevator_object.door_open = True
    elevator_object.status = 0
    logger.info(f"elevator status: HALT")
    elevator_object.door_open = False
    logger.info(
        f"elevator: {elevator_object.elevator_system_id.name}:{elevator_object.elevator_id} door closing")
    elevator_object.save()
    return elevator_object


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
    """process request for provided system

    Args:
        elevator_system (ElevatorSystem): elevator_system which is being processed currently
    """
    requests_pending = ElevatorRequest.objects.filter(
        elevator_system=elevator_system,
        is_active=True,
    ).order_by('request_time')

    for elev_request in requests_pending:
        logger.info(
            f"fetching pending request for elevator system: {elevator_system.elevator_system_id}")

        logger.debug(f"processing request: {elev_request}")
        request_start = elev_request.requested_floor
        request_destination = elev_request.destination_floor

        logger.debug(f"fetching nearest elevator for request: {elev_request}")
        elevator_object = get_nearest_elevator(elevator_system, request_start)
        elev_request.elevator = elevator_object
        elev_request.save()
        logger.info(
            f"selected closest elevator: {elevator_object.elevator_id}, elevator system: {elevator_system.elevator_system_id}")
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
        elevator_object = move_to_floor(request_start, elevator_object)
        elevator_object.save()

        # Let people get in, Close the door
        elevator_object.door_open = False

        # move to elevator to destination floor
        elevator_object = move_to_floor(request_destination, elevator_object)
        elevator_object.save()

        elev_request.is_active = False
        elev_request.save()


def final_run():
    """process request for each system continuosly
    """
    elevator_systems = ElevatorSystem.objects.all().order_by('elevator_system_id')

    try:
        for elevator_system in elevator_systems:
            process_request(elevator_system=elevator_system)
    except Exception as exc:
        print(exc)
