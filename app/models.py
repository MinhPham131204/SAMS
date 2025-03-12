from django.db import models
from django.db.models import Q, F
from django.db.models.constraints import CheckConstraint


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.username
    
    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(password__regex=r'.{8,}'),
                name='password_min_length_8'
            )
        ]
    
class Sensor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Threshold(models.Model):
    sensorID = models.OneToOneField(Sensor, on_delete=models.CASCADE, primary_key=True)
    lowerTemp = models.FloatField()
    upperTemp = models.FloatField()
    lowerHumidity = models.FloatField()
    upperHumidity = models.FloatField() 
    lowerLight = models.FloatField()
    upperLight = models.FloatField()
    lowerSoil = models.FloatField()
    upperSoil = models.FloatField()
    
    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(lowerTemp__lt=F('upperTemp')),
                name='check_lower_temp_lt_upper_temp'
            ),
            CheckConstraint(
                check=Q(lowerHumidity__lt=F('upperHumidity')),
                name='check_lower_humidity_lt_upper_humidity'
            ),
            CheckConstraint(
                check=Q(lowerLight__lt=F('upperLight')),
                name='check_lower_light_lt_upper_light'
            ),
            CheckConstraint(
                check=Q(lowerSoil__lt=F('upperSoil')),
                name='check_lower_soil_lt_upper_soil'
            )
        ]

class Schedule(models.Model):
    sensorID = models.OneToOneField(Sensor, on_delete=models.CASCADE, primary_key=True)
    ventilatedTime = models.TimeField()
    irrigatedTime = models.TimeField()

class VentilateDaily(models.Model):
    sensorID = models.ForeignKey(Sensor, on_delete=models.CASCADE, verbose_name='sensorID')
    ventilatedTime = models.TimeField()

class IrrigateDaily(models.Model):
    sensorID = models.ForeignKey(Sensor, on_delete=models.CASCADE, verbose_name='sensorID')
    irrigatedTime = models.TimeField() 