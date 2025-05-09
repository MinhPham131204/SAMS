from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import json
from ..models import Schedule, IrrigateDaily, VentilateDaily, Sensor

load_dotenv()

@csrf_exempt
def getSchedule(request, id):
    irrigateDaily = IrrigateDaily.objects.filter(sensorID=id).values()
    ventilateDaily = VentilateDaily.objects.filter(sensorID=id).values()
    return JsonResponse({'irrigateDaily': list(irrigateDaily), 'ventilateDaily': list(ventilateDaily)})

@csrf_exempt
@require_http_methods(['POST'])
def irrigateSchedule(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if Schedule.objects.filter(sensorID=body["sensorID"]).values():
        Schedule.objects.filter(sensorID=body["sensorID"]).update(
            irrigatedTime=body["irrigatedTime"],
        )
        Schedule.objects.filter(sensorID=body["sensorID"]).update(
            irrigatedDuration=body["irrigatedDuration"],
        )
        return JsonResponse({'status': 'success'})
    else:
        sensor = Sensor.objects.filter(id=body["sensorID"]).first()
        if sensor:
            schedule = Schedule(sensorID=sensor, irrigatedTime=body['irrigatedTime'])
            schedule.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({"message": "Không tìm thấy sensor"})
    
@csrf_exempt
@require_http_methods(['POST'])
def ventilateSchedule(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if Schedule.objects.filter(sensorID=body["sensorID"]).values():
        Schedule.objects.filter(sensorID=body["sensorID"]).update(
            ventilatedTime=body["ventilatedTime"],
        )
        Schedule.objects.filter(sensorID=body["sensorID"]).update(
            ventilatedDuration=body["ventilatedDuration"],
        )
        return JsonResponse({'status': 'success'})
    else:
        sensor = Sensor.objects.filter(id=body["sensorID"]).first()
        if sensor:
            schedule = Schedule(sensorID=sensor, ventilatedTime=body['ventilatedTime'])
            schedule.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({"message": "Không tìm thấy sensor"})

@csrf_exempt
@require_http_methods(['POST'])
def irrigateDaily(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    sensor = Sensor.objects.filter(id=body["sensorID"]).first()
    if sensor:
        schedule = IrrigateDaily(sensorID=sensor, irrigatedTime=body['irrigatedTime'])
        schedule.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({"message": "Không tìm thấy sensor"})

@csrf_exempt
@require_http_methods(['POST'])
def ventilateDaily(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    sensor = Sensor.objects.filter(id=body["sensorID"]).first()
    if sensor:
        schedule = VentilateDaily(sensorID=sensor, ventilatedTime=body['ventilatedTime'])
        schedule.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({"message": "Không tìm thấy sensor"})
 