from fire_managment.helpers.deserializer import Deserializer
from .interface import SelectPointsPayload, CreatePointPayload, SensorInputPayload, MonitoringPayload, DefineUser
from django.http import JsonResponse
from fire_managment.models import Sensor
from fire_managment.helpers.get_area import findGroups, getGroupLines


USERS = {}
SENSORES = []
TEMPERATURE_WARNING = 40
TEMPERATURE_BURNING = 100
SMOKE_LEVEL_WARNING = 1
SMOKE_LEVEL_BURNING = 2


class MapController(Deserializer):
    
    def __init__(self, request, kwargs=None):
        Deserializer.__init__(self, request=request, kwargs=kwargs)
        coordinates = [
                ((0.0, 0.0), 2),
                ((0.0, 300), 2),
                ((0.0, 600), 2),
                ((300, 0.0), 0),
                ((300, 300), 0),
                ((300, 600), 2),
                ((600, 0.0), 2),
                ((600, 300), 2),
                ((600, 600), 2),
        ]
        for i in range(len(coordinates)):
            sensor = Sensor(id=i,x=coordinates[i][0][0], y=coordinates[i][0][1], is_burning = coordinates[i][1])
            SENSORES.append(sensor)
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
                x=params.longitude,
                y=params.latitude,
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
    


    def monitorar_area(self):
        # params:MonitoringPayload = self.deserialize(model=MonitoringPayload)
        # latitude = params.latitude
        # longitude = params.longitude
        # distancia = params.distancia
        grups = findGroups(SENSORES)
        counter = 1
        data = {}
        for group in grups:
            sensors = [{'id':idx, 'x':SENSORES[idx].coordinates[0], 'y':SENSORES[idx].coordinates[1]} for idx in group]
            try:
                lines, area, perimeter = getGroupLines(group, SENSORES)
            except:
                lines = []
                area = 0
                perimeter = 0
            data[f'firehotspot{counter}'] = {'convex_hull_lines': lines, 'sensors_alerting': sensors, 'area_meters_2': area, 'perimeter_meters': perimeter}

        return JsonResponse(data, status=200)
        
    def register_user(self):
        params:DefineUser = self.deserialize(model=DefineUser)
        x1 = params.x_1
        x2 = params.X_2
        y1 = params.y_1
        y2 = params.y_2
        for sensor in SENSORES:
            sensor:Sensor
            if sensor.coordinates[0] > x1 and sensor.coordinates[0] < x2 and sensor.coordinates[1] > y1 and sensor.coordinates[1] < y2:
                USERS[params.user_id].append(sensor.id)
        return JsonResponse(f"Usuario com id {params.user_id} registrado com sucesso !")