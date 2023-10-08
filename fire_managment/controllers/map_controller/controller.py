from fire_managment.helpers.deserializer import Deserializer
from .interface import SelectPointsPayload, CreatePointPayload, SensorInputPayload, MonitoringPayload
from django.http import JsonResponse
from fire_managment.models import Sensor


USERS = {}
SENSORES = []
TEMPERATURE_WARNING = 40
TEMPERATURE_BURNING = 100
SMOKE_LEVEL_WARNING = 1
SMOKE_LEVEL_BURNING = 2


class MapController(Deserializer):
    
    def __init__(self, request, kwargs=None):
        Deserializer.__init__(self, request=request, kwargs=kwargs)

        # params:SelectPointsPayload = self.deserialize(model=SelectPointsPayload)
        # latitude = params.l
        # longitude = params.x_2
        # sensors = Sensor.objects.filter(
        #     position_x__gte=x1, 
        #     position_x__lte=x2, 
        #     position_y__gte=y1, 
        #     position_y__lte=y2
        #     ).values('id','position_x','position_y')

        # return JsonResponse({
        #     'data': list(sensors)
        # }, status=200)
    
    def create_point(self):
        params:CreatePointPayload= self.deserialize(model=CreatePointPayload)
        try:
            sensor:Sensor = Sensor(
                id = params.id,
                latitude=params.longitude,
                longitude=params.latitude,
            )
            SENSORES.append(sensor)
        except:
            return JsonResponse({
                'message': "An error has ocurred"
            }, status=400)
        return JsonResponse({
            'message': f"Sensor with id {params.id} added with success"
        }, status=200)
    
    
    @staticmethod    
    def check_level(sensor:Sensor, smoke_level, temperature_level):
        if smoke_level > SMOKE_LEVEL_BURNING or temperature_level > TEMPERATURE_BURNING:
            is_burning = 2
        elif smoke_level > SMOKE_LEVEL_WARNING or temperature_level > TEMPERATURE_WARNING:
            is_burning = 1
        else:
            is_burning = 0
        return is_burning


    def sensor_input(self):
        params:SensorInputPayload = self.deserialize(model=SensorInputPayload)
        try:
            for sensor in SENSORES:
                sensor:Sensor
                if sensor.id == params.id:
                    sensor.update_sensor(temperature=params.temperature, smoke_level=params.smoke_level)
                    sensor.is_burning = self.check_level(sensor=sensor, smoke_level= params.smoke_level, temperature_level= params.temperature)
                    if sensor.is_burning == 1:
                        for key in USERS:
                            if USERS[key].id == sensor.id:
                                return JsonResponse({
                                    "message": f"sensor id {sensor.id} is on risk to burn"
                                })
                    if sensor.is_burning == 2:
                        for key in USERS:
                            if USERS[key].id == sensor.id:
                                return JsonResponse({
                                    "message": f"sensor id {sensor.id} is burning"
                                })

        except:
            return JsonResponse({
                'message': "An error has ocurred"
            }, status=400)

        return JsonResponse({
            'message': f"Sensor with id {params.id} updated with success"
        }, status=200)
    
    def convex_hull(self):
        pass


    def monitorar_area(self):
        params:MonitoringPayload = self.deserialize(model=MonitoringPayload)
        latitude = params.latitude
        longitude = params.longitude
        distancia = params.distancia

        for sensor in SENSORES:
            pass
    