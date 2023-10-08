from django.db import models
from fire_managment.helpers.get_area import convLatLonToXY


class Sensor:
    def __init__(self,id, x, y, temperature = None, smoke_level = None, is_burning = None):
        self.id = id
        self.coordinates = (x,y)
        self.temperature = temperature
        self.smoke_level = smoke_level
        self.is_burning = is_burning


    def update_sensor(self, temperature, smoke_level):
        self.temperature = temperature
        self.smoke_level = smoke_level
    

class User:
    def __init__(self, list_of_sensors:list):
        self.list_of_ids = list_of_sensors

