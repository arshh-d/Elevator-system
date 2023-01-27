from django.shortcuts import render
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpRequest
from .models import Elevator, ElevatorSystem
from .utils import create_elevators
# Create your views here.


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

    create_elevators(
        system_id=payload.get("system_id"),
        system_name=payload.get("system_name"),
        max_floor=payload.get("max_floor"),
        count=payload.get("elevator_count"))

    return JsonResponse({"msg": "created elevator"}, status=200)


@require_http_methods(['GET'])
def get_all_elevators(request: HttpRequest, system_id: int) -> JsonResponse:
    """List all the elevators details of given elevator system

    Args:
        request (HttpRequest): request body
        system_id (int): system_id of the elevator system

    Returns:
        JsonResponse: list of all the elevators in the system
    """

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
    elevators = Elevator.objects.filter(
        elevator_system_id_id=system_id,
        elevator_id=elevator_id
    ).values()

    elevator_list = []
    for ele in elevators:
        elevator_list.append(ele)

    response = {
        "elevators": elevator_list
    }

    return JsonResponse(response, status=200)
