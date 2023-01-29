import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from .models import Elevator, ElevatorSystem, ElevatorRequest
from .utils import create_elevators
from loguru import logger


@csrf_exempt
@require_http_methods(['POST'])
def create_elevator_system(request: HttpRequest) -> JsonResponse:
    """Initializes an elevator system

    Args:
        request (HttpRequest): param for intializing the elevator_system

    Returns:
        JsonResponse: status response
    """
    payload = json.loads(request.body.decode('utf-8'))
    logger.info(
        f"creating elevator system with id: {payload.get('system_id')}")
    create_elevators(
        system_id=payload.get("system_id"),
        system_name=payload.get("system_name"),
        max_floor=payload.get("max_floor"),
        count=payload.get("elevator_count"))
    logger.info(f"elevator system: {payload.get('system_id')} initialized")
    return JsonResponse({"msg": "created elevator"}, status=200)


@csrf_exempt
@require_http_methods(['GET'])
def get_all_elevators(request: HttpRequest, system_id: int) -> JsonResponse:
    """List all the elevators details of given elevator system

    Args:
        request (HttpRequest): request body
        system_id (int): system_id of the elevator system

    Returns:
        JsonResponse: list of all the elevators in the system
    """
    logger.info(f"listing all elevator in elevator system: {system_id}")
    elevators = Elevator.objects.filter(
        elevator_system_id_id=system_id).values()

    elevator_list = []
    for ele in elevators:
        elevator_list.append(ele)

    response = {
        "elevators": elevator_list
    }
    return JsonResponse(response, status=200)


@require_http_methods(['GET'])
def get_elevator(request: HttpRequest, system_id: int, elevator_id: int) -> JsonResponse:
    """Lists details of a single elevator

    Args:
        request (HttpRequest): request
        system_id (int): system_id to which the elevator belongs
        elevator_id (int): elevator number

    Returns:
        JsonResponse: details of the selected elevator
    """
    logger.info(
        f"fetching details for elevator: {elevator_id}, system_id: {system_id}")
    elevators = Elevator.objects.filter(
        elevator_system_id_id=system_id,
        elevator_id=elevator_id
    ).values()

    elevator_list = []
    for ele in elevators:
        elevator_list.append(ele)
    logger.info(
        f"feteched details for elevator: {elevator_id}, system_id: {system_id}")
    response = {
        "elevators": elevator_list
    }
    return JsonResponse(response, status=200)


@csrf_exempt
@require_http_methods(['POST'])
def create_request(request):

    payload = json.loads(request.body.decode('utf-8'))

    elevator = Elevator.objects.get(
        elevator_system_id_id=payload.get('system_id'),
        elevator_id=payload.get('elevator_id')
    )
    logger.info(f"creating new request for system: {payload.get('system_id')}")
    new_request = ElevatorRequest.objects.create(
        elevator=elevator,
        elevator_system_id=payload.get('system_id'),
        requested_floor=payload.get('requested_floor'),
        destination_floor=payload.get('destination_floor'),
    )
    new_request.save()
    logger.info(f"request created for system: {payload.get('system_id')}")
    response = {"msg": "resquest accepted"}
    return JsonResponse(response, status=200)
