from django.http import JsonResponse, HttpResponse
from functools import wraps
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from Adafruit_IO import Client, MQTTClient
from dotenv import load_dotenv
import os, pytz, json, requests
from datetime import datetime
from .models import User, Threshold, Schedule, IrrigateDaily, VentilateDaily, Sensor, Enviroment_log, Device_state
from django.utils import timezone
from datetime import timedelta

def format_datetime(dt_string):
    if dt_string.endswith('Z'):
        dt_string = dt_string.replace('Z', '+00:00')

    dt = datetime.fromisoformat(dt_string)

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

def allow_cors(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Origin, Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

    return wrapped_view

@allow_cors
def getData(request):
    try:
        # Lấy tham số khoảng thời gian từ request
        range_minute = int(request.GET.get('range_minute', 60))  # Mặc định 60 phút nếu không có
        
        # Tính toán thời gian bắt đầu dựa trên range_minute
        time_threshold = timezone.now() - timedelta(minutes=range_minute)
        
        # Truy vấn dữ liệu sử dụng Django ORM
        logs = Enviroment_log.objects.filter(timestamp__gte=time_threshold).order_by('-timestamp')
        
        # Chuyển đổi queryset thành danh sách các dictionaries
        data = []
        for log in logs:
            log_dict = model_to_dict(log)
            # Định dạng timestamp để hiển thị dễ đọc
            log_dict['timestamp'] = format_datetime(log_dict['timestamp'].isoformat())
            data.append(log_dict)
            
        return JsonResponse({
            "success": True,
            "data": data,
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        })

@csrf_exempt
def yolobit_api(request):
    # Validate Method
    if request.method != "POST":
        return HttpResponse("", status=404)

    # Parse JSON
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        # Extract data
        temperature = float(data.get("temp"))
        humidity = float(data.get("hum"))
        light = float(data.get("lig"))
        soil = float(data.get("soil"))
        
        # Lưu dữ liệu sử dụng Django ORM
        log_entry = Enviroment_log(
            temperature=temperature,
            humidity=humidity,
            light=light,
            soil=soil,
            timestamp=timezone.now()
        )
        log_entry.save()
        
        device_status = list(Device_state.objects.values())
        
        # Trả về kết quả
        return JsonResponse({
            "success": True,
            "data": device_status
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)

def turnOnWatering(request):
    client.publish('bbc-manual-watering', 1)
    return JsonResponse({'status': 1})

def turnOffWatering(request):
    client.publish('bbc-manual-watering', 0)   
    return JsonResponse({'status': 0})

def turnOnVentilate(request):
    client.publish('bbc-manual-temperature', 1)
    return JsonResponse({'status': 1})

def turnOffVentilate(request):
    client.publish('bbc-manual-temperature', 0)    
    return JsonResponse({'status': 0})

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
        return JsonResponse({
            'status': 'success',
            'data': body
        })
    else: 
        return JsonResponse({"message": "Không tìm thấy sensor"})

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
        return JsonResponse({'status': 'success'})
    else:
        sensor = Sensor.objects.filter(id=body["sensorID"]).first()
        if sensor:
            schedule = Schedule(sensorID=sensor, irrigatedTime=body['irrigatedTime'], ventilatedTime="00:00:00")
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
        return JsonResponse({'status': 'success'})
    else:
        sensor = Sensor.objects.filter(id=body["sensorID"]).first()
        if sensor:
            schedule = Schedule(sensorID=sensor, ventilatedTime=body['ventilatedTime'], irrigatedTime="00:00:00")
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
    
@csrf_exempt
@require_http_methods(['POST'])
def handleHumidity(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    humi = Threshold.objects.filter(sensorID=body["sensorID"]).values_list('lowerHumidity', 'upperHumidity')
    if humi:
        # humidity < lower threshold of humidity
        if body["humidity"] < humi[0][0]:
            client.publish('bbc-manual-watering', 1)
            Device_state.objects.filter(device_name="water_pump").update(state=1)
            return JsonResponse({'status': 'Độ ẩm thấp hơn mức cho phép. Đang tưới nước'})
        
        # humidity > upper threshold of humidity
        elif body["humidity"] > humi[0][1]: 
            client.publish('bbc-manual-temperature', 1)
            Device_state.objects.filter(device_name="mini_fan").update(state=1)
            return JsonResponse({'status': 'Độ ẩm cao hơn mức cho phép. Đang thông gió'})
        
        # humidity in range
        else:
            if (Device_state.objects.filter(device_name="water_pump").values())[0]['state'] == 1:
                requests.get('/turnOffWatering')
                Device_state.objects.filter(device_name="water_pump").update(state=1) 
            elif (Device_state.objects.filter(device_name="mini_fan").values())[0]['state'] == 1:
                requests.get('/turnOffVentilate')
                Device_state.objects.filter(device_name="mini_fan").update(state=1)   

            return JsonResponse({'status': 'Độ ẩm ở mức cho phép'})
    else:
        return JsonResponse({"message": "Không tìm thấy sensor"})

@csrf_exempt
@require_http_methods(['POST'])
def handleTemperature(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    temp = Threshold.objects.filter(sensorID=body["sensorID"]).values_list('lowerTemp', 'upperTemp')
    if temp:
        # temperature < lower threshold of temperature
        if body["temperature"] < temp[0][0]:
            if (Device_state.objects.filter(device_name="mini_fan").values())[0]['state'] == 1:
                client.publish('bbc-manual-temperature', 0)
                Device_state.objects.filter(device_name="mini_fan").update(state=1)
            return JsonResponse({'status': 'Nhiệt độ thấp hơn mức cho phép. Đã tắt quạt'})
        
        # temperature > upper threshold of temperature
        elif body["temperature"] > temp[0][1]:
            client.publish('bbc-manual-temperature', 1)
            Device_state.objects.filter(device_name="mini_fan").update(state=1)

            client.publish('bbc-manual-watering', 0)
            Device_state.objects.filter(device_name="water_pump").update(state=1)
            return JsonResponse({'status': 'Nhiệt độ cao hơn mức cho phép. Đang thông gió và tưới nước'})
        
        # temperature in range
        else:
            if (Device_state.objects.filter(device_name="water_pump").values())[0]['state'] == 1:
                requests.get('/turnOffWatering')
                Device_state.objects.filter(device_name="water_pump").update(state=1) 
            elif (Device_state.objects.filter(device_name="mini_fan").values())[0]['state'] == 1:
                requests.get('/turnOffVentilate')
                Device_state.objects.filter(device_name="mini_fan").update(state=1)  
            return JsonResponse({'status': 'Nhiệt độ ở mức cho phép'})
    else:
        return JsonResponse({"message": "Không tìm thấy sensor"})
    
@csrf_exempt
@require_http_methods(['POST'])
def updateMode(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if body["type"] == "irrigation":
        Device_state.objects.filter(device_name="water_pump").update(manualMode=body["mode"])
        return JsonResponse({
            "success": True,
            'data': body["mode"]
        })
    elif body["mode"] == "ventilation":
        Device_state.objects.filter(device_name="mini_fan").update(manualMode=body["mode"])
        return JsonResponse({
            "success": True,
            'data': body["mode"]
        })
    else:
        return JsonResponse({
            "success": False,
            "error": "Không tìm thấy chế độ"
        })
    
@csrf_exempt
@require_http_methods(['POST'])
def updateState(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if body["type"] == "irrigation":
        if not Device_state.objects.filter(device_name="water_pump").first().manualMode: 
            return JsonResponse({
                "success": False,
                "error": "Bạn đang ở chế độ tự động, không thể thực hiện hành động này."
            })
        
        Device_state.objects.filter(device_name="water_pump").update(state=body["state"])
        return JsonResponse({
            "success": True,
            'data': body["state"]
        })
    
    elif body["type"] == "ventilation":
        if not Device_state.objects.filter(device_name="mini_fan").first().manualMode: 
            return JsonResponse({
                "success": False,
                "error": "Bạn đang ở chế độ tự động, không thể thực hiện hành động này."
            })
        
        Device_state.objects.filter(device_name="mini_fan").update(state=body["state"])
        return JsonResponse({
            "success": True,
            'data': body["state"]
        })
    else:
        return JsonResponse({
            "success": False,
            "error": "Không tìm thấy chế độ"
        })