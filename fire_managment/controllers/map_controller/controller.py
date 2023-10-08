from fire_managment.helpers.deserializer import Deserializer
from .interface import SelectPointsPayload, CreatePointPayload, SensorInputPayload
from django.http import JsonResponse
from fire_managment.models import Sensor


class MapController(Deserializer):
    
    def __init__(self, request, kwargs=None):
        Deserializer.__init__(self, request=request, kwargs=kwargs)

    def select_point(self):
        params:SelectPointsPayload = self.deserialize(model=SelectPointsPayload)
        x1 = params.x_1
        x2 = params.x_2
        y1 = params.y_1
        y2 = params.y_2
        sensors = Sensor.objects.filter(
            position_x__gte=x1, 
            position_x__lte=x2, 
            position_y__gte=y1, 
            position_y__lte=y2
            ).values('id','position_x','position_y')

        return JsonResponse({
            'data': list(sensors)
        }, status=200)
    
    def create_point(self):
        params:CreatePointPayload= self.deserialize(model=CreatePointPayload)
        try:
            sensor = Sensor(
                id = params.id,
                position_x=params.position_x,
                position_y=params.position_y,
            )
            sensor.save()
        except:
            return JsonResponse({
                'message': "An error has ocurred"
            }, status=400)
        return JsonResponse({
            'message': f"Sensor with id {params.id} added with success"
        }, status=200)
    
    def sensor_input(self):
        params:SensorInputPayload = self.deserialize(model=SensorInputPayload)
        try:
            sensor = Sensor.objects.get(id=params.id)
            sensor.temperature = params.temperature
            sensor.smoke_level = params.smoke_level
            sensor.save()
        except:
            return JsonResponse({
                'message': "An error has ocurred"
            }, status=400)
        
        return JsonResponse({
            'message': f"Sensor with id {params.id} updated with success"
        }, status=200)
    
    def convex_hull(self):
        pass