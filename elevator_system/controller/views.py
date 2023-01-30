import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from .models import Elevator, ElevatorRequest
from .utils import create_elevators
from loguru import logger


error_response = {"msg": "error while querying database, invalid details"}

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
    response = {"msg": ""}
    logger.info(
        f"creating elevator system with id: {payload.get('system_id')}")
    created = create_elevators(
        system_id=payload.get("system_id"),
        system_name=payload.get("system_name"),
        max_floor=payload.get("max_floor"),
        count=payload.get("elevator_count"))
    if created:
        logger.info(f"elevator system: {payload.get('system_id')} initialized")
        response["msg"] = "created elevator"
        status_code = 200
    else:
        response["msg"] = "error in system creation"
        status_code = 400
    return JsonResponse(response, status=status_code)


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
    try:
        elevators = Elevator.objects.filter(
            elevator_system_id_id=system_id).values()
    except Exception as exception:
        logger.error(
            f"invalid details received, exception caused by: {exception}")
        return JsonResponse(error_response, status=400)
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
    try:
        elevators = Elevator.objects.filter(
            elevator_system_id_id=system_id,
            elevator_id=elevator_id
        ).values()
    except Exception as exception:
        logger.error(
            f"invalid details received, exception caused by: {exception}")
        return JsonResponse(error_response, status=400)

    elevator_list = []
    for ele in elevators:
        elevator_list.append(ele)
    logger.info(
        f"fetched details for elevator: {elevator_id}, system_id: {system_id}")
    response = {
        "elevators": elevator_list
    }
    return JsonResponse(response, status=200)


@csrf_exempt
@require_http_methods(['POST'])
def create_request(request: HttpRequest) -> JsonResponse:
    """create a new request

    Args:
        request (HttpRequest): payload with request details

    Returns:
        JsonResponse: success message with relevant status code 
    """
    payload = json.loads(request.body.decode('utf-8'))
    try:
        elevator = Elevator.objects.get(
            elevator_system_id_id=payload.get('system_id'),
            elevator_id=payload.get('elevator_id')
        )
        logger.info(
            f"creating new request for system: {payload.get('system_id')}")
    except Exception as exception:
        logger.error(
            f"invalid details received, exception caused by: {exception}")
        return JsonResponse(error_response, status=400)
    new_request = ElevatorRequest.objects.create(
        elevator=elevator,
        elevator_system_id=payload.get('system_id'),
        requested_floor=payload.get('requested_floor'),
        destination_floor=payload.get('destination_floor'),
    )
    new_request.save()
    logger.info(f"request created for system: {payload.get('system_id')}")
    response = {"msg": "request created"}
    return JsonResponse(response, status=200)


@csrf_exempt
@require_http_methods(['POST'])
def update_elevator_status(request) -> JsonResponse:
    """marks the given elevator as working or not working.

    Args:
        request (_type_): padyload with details of the elevator to update
    """
    payload = json.loads(request.body.decode('utf-8'))
    try:
        elevator = Elevator.objects.get(
            elevator_system_id=payload.get('system_id'),
            elevator_id=payload.get("elevator_id")
        )
    except Exception as exception:
        logger.error(
            f"invalid details received, exception caused by: {exception}")
        return JsonResponse(error_response, status=400)
    elevator.working = payload.get('working')
    elevator.save()
    logger.info(
        f"elevator: {elevator.elevator_system_id.name}:{elevator.elevator_id} updated working status to: {elevator.working}")
    response = {
        "msg": "elevator status updated"
    }
    return JsonResponse(response, status=200)
