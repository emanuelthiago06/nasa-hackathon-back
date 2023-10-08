from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from fire_managment.controllers.map_controller.controller import MapController
from fire_managment.helpers.validor_request import validate_request
from fire_managment.controllers.map_controller.interface import CreatePointPayload, SelectPointsPayload
# Create your views here.


@api_view(["POST"])
def view_map(request):
    pass

@api_view(['GET'])
@validate_request(SelectPointsPayload)
def select_points(request, **kwargs):
    map_controller = MapController(request=request, kwargs=kwargs)
    return map_controller.select_point()


@api_view(['POST'])
@validate_request(CreatePointPayload)
def add_points(request, **kwargs):
    map_controller = MapController(request=request, kwargs=kwargs)
    return map_controller.create_point()


@api_view(['POST'])
def monitor_area(request, **kwargs):
    map_controller = MapController(request=request, kwargs=kwargs)
    return map_controller.monitorar_area()
    

@api_view(['POST'])
def register_user(request, **kwargs):
    map_controller = MapController(request=request, kwargs= kwargs)
    return map_controller.register_user()