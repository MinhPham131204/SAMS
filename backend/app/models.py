from django.db import models
from django.db.models import Q, F
from django.db.models.constraints import CheckConstraint
from django.utils import timezone as django_timezone  # Add this import


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
    ventilatedTime = models.DateTimeField(null=True, blank=True)
    irrigatedTime = models.DateTimeField(null=True, blank=True)
    irrigatedDuration = models.IntegerField()
    ventilatedDuration = models.IntegerField()

class VentilateDaily(models.Model):
    sensorID = models.ForeignKey(Sensor, on_delete=models.CASCADE, verbose_name='sensorID')
    startTime = models.TimeField(null=True) 
    endTime = models.TimeField(null=True)

class IrrigateDaily(models.Model):
    sensorID = models.ForeignKey(Sensor, on_delete=models.CASCADE, verbose_name='sensorID')
    startTime = models.TimeField(null=True) 
    endTime = models.TimeField(null=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(startTime__lt=F('endTime')),
                name='check_start_time_lt_end_time'
            )
        ]

class Enviroment_log(models.Model):
    timestamp = models.DateTimeField(primary_key=True, default=django_timezone.now)
    temperature = models.FloatField()
    humidity = models.FloatField()
    light = models.FloatField()
    soil = models.FloatField()

class Device_state(models.Model):
    device_name = models.CharField(max_length=50, unique=True, db_collation='utf8mb4_unicode_ci')
    state = models.BooleanField()
    manualMode = models.BooleanField(default=True)