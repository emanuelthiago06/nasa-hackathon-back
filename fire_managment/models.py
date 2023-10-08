from django.db import models

class Sensor(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    position_x = models.IntegerField(null=False)
    position_y = models.IntegerField(null=False)
    temperature = models.IntegerField(null=True,blank=True)
    smoke_level = models.IntegerField(null=True,blank=True)