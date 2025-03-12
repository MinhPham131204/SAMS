from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from Adafruit_IO import Client, MQTTClient
from dotenv import load_dotenv
import os, pytz, json
from datetime import datetime
from .models import User, Threshold, Schedule, IrrigateDaily, VentilateDaily

def format_datetime(dt_string):
    if dt_string.endswith('Z'):
        dt_string = dt_string.replace('Z', '+00:00')
        
        # Parse the ISO datetime string with timezone info
    dt = datetime.fromisoformat(dt_string)
    
    # Option 1: Convert to Vietnam timezone (UTC+7)
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    dt = dt.astimezone(vietnam_tz)

    return dt.strftime("%Y/%m/%d %H:%M:%S")


load_dotenv()

AIO_USERNAME = os.getenv('AIO_USERNAME')
AIO_KEY = os.getenv('AIO_KEY')

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.connect()
client.loop_background()

aio = Client(AIO_USERNAME, AIO_KEY)


def getData(request):
    temperature_feeds = aio.data('bbc-temperature')
    light_feeds = aio.data('bbc-light')
    humidity_feeds = aio.data('bbc-humidity')
    soil_feeds = aio.data('bbc-soil-moisture')
    temp_threshold = aio.data('bbc-temperature-threshold')
    soil_threshold = aio.data('bbc-soil-moisture-threshold')
    
    data = {
        'temperature': temperature_feeds[0].value,
        'light': light_feeds[0].value,
        'humidity': humidity_feeds[0].value,
        'soilMoisture': soil_feeds[0].value,
        'tempThreshold': temp_threshold[0].value,
        'soilThreshold': soil_threshold[0].value,
        'humidityHistory': [(x.value, format_datetime(x[1])) for x in humidity_feeds[0:30]],
        'temperatureHistory': [(x.value, format_datetime(x[1])) for x in temperature_feeds[0:30]],
        'lightHistory': [(x.value, format_datetime(x[1])) for x in light_feeds[0:30]],
        'soilMoistureHistory': [(x.value, format_datetime(x[1])) for x in soil_feeds[0:30]]
    }
    return JsonResponse(data)

def manualWatering(request):
    status = aio.data('bbc-manual-watering')
    client.publish('bbc-manual-watering', 1 - int(status[0].value))
    return JsonResponse({'status': 1 - int(status[0].value)})

def manualVentilate(request):
    status = aio.data('bbc-manual-temperature')
    client.publish('bbc-manual-temperature', 1 - int(status[0].value))
    return JsonResponse({'status': 1 - int(status[0].value)})

@csrf_exempt
@require_http_methods(['POST'])
def login(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    user = User.objects.filter(email=body['email'], password=body['password']).values()
    return JsonResponse({'status': 'success'}) if user else JsonResponse({'status': 'failed'})

@csrf_exempt
@require_http_methods(['POST'])
def signup(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    checkEmail = User.objects.filter(email=body['email']).values()
    checkPhone = User.objects.filter(phone=body['phone']).values()
    if checkEmail:
        return JsonResponse({"message":"Email này đã đăng kí"})
    if checkPhone:
        return JsonResponse({"message":"Số điện thoại này đã đăng kí"})
    user = User(username=body['username'], password=body['password'], email=body['email'], phone=body['phone'])
    user.save()
    return JsonResponse({'status': 'success'})

def getThreshold(request, id):
    threshold = Threshold.objects.filter(sensorID=id).values()
    return JsonResponse(threshold[0])

@csrf_exempt
@require_http_methods(['PUT'])
def config(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if Threshold.objects.filter(sensorID=body["sensorID"]).values():
        Threshold.objects.filter(sensorID=body["sensorID"]).update(
            lowerTemp=body["lowerTemp"],
            upperTemp=body["upperTemp"],
            lowerHumidity=body["lowerHumidity"],
            upperHumidity=body["upperHumidity"],
            lowerLight=body["lowerLight"],
            upperLight=body["upperLight"],
            lowerSoil=body["lowerSoil"],
            upperSoil=body["upperSoil"]
        )
        return JsonResponse({'status': 'success'})
    else: 
        return JsonResponse({"message": "Không tìm thấy sensor"})

def getSchedule(request, id):
    irrigateDaily = IrrigateDaily.objects.filter(id=id).values()
    ventilateDaily = VentilateDaily.objects.filter(sensorID=id).values()
    return JsonResponse({'irrigateDaily': list(irrigateDaily), 'ventilateDaily': list(ventilateDaily)})

@csrf_exempt
@require_http_methods(['POST'])
def irrigateSchedule(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if Schedule.objects.filter(sensorID=body["sensorID"]).values():
        Schedule.objects.filter(sensorID=body["sensorID"]).update(
            irrigateTime=body["irrigateTime"],
        )
        return JsonResponse({'status': 'success'})
    else:
        schedule = Schedule(sensorID=body['sensorID'], irrigateTime=body['irrigateTime'])
        schedule.save()
        return JsonResponse({'status': 'success'})
    
@csrf_exempt
@require_http_methods(['POST'])
def ventilateSchedule(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if Schedule.objects.filter(sensorID=body["sensorID"]).values():
        Schedule.objects.filter(sensorID=body["sensorID"]).update(
            ventilateTime=body["ventilateTime"],
        )
        return JsonResponse({'status': 'success'})
    else:
        schedule = Schedule(sensorID=body['sensorID'], ventilateTime=body['ventilateTime'])
        schedule.save()
        return JsonResponse({'status': 'success'})
    
@csrf_exempt
@require_http_methods(['POST'])
def irrigateDaily(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    schedule = Schedule(sensorID=body['sensorID'], irrigateTime=body['irrigateTime'])
    schedule.save()
    return JsonResponse({'status': 'success'})

@csrf_exempt
@require_http_methods(['POST'])
def ventilateDaily(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    schedule = Schedule(sensorID=body['sensorID'], ventilateTime=body['ventilateTime'])
    schedule.save()
    return JsonResponse({'status': 'success'})