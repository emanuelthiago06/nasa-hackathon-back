from django.db import models

class Sensor:
    def __init__(self,id, latitude, longitude):
        self.id = id
        self.coordinates = (latitude,longitude)
        self.temperature = None
        self.smoke_level = None
        self.is_burning = False


    def update_sensor(self, temperature, smoke_level):
        self.temperature = temperature
        self.smoke_level = smoke_level
    

class User:
    def __init__(self, list_of_sensors:list):
        self.list_of_ids = list_of_sensors

