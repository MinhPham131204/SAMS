from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from dotenv import load_dotenv
import pytz, json
from datetime import datetime
from .models import User, Threshold, Schedule, IrrigateDaily, VentilateDaily, Sensor, Enviroment_log, Device_state
from django.utils import timezone
from datetime import timedelta

load_dotenv()

def checkAutoModePump():
    return 1 - Device_state.objects.filter(device_name="water_pump").first().manualMode

def checkAutoModeFan():
    return 1 - Device_state.objects.filter(device_name="mini_fan").first().manualMode

@csrf_exempt
@require_http_methods(['POST'])
def handleHumidity(request):
    if not checkAutoModePump() and not checkAutoModeFan():
        return JsonResponse({
            "success": False,
            "error": "Bạn đang ở chế độ thủ, không thể thực hiện hành động này."
        })
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    humi = Threshold.objects.filter(sensorID=body["sensorID"]).values_list('lowerHumidity', 'upperHumidity')
    if humi:
        # humidity < lower threshold of humidity
        if body["humidity"] < humi[0][0]:
            # client.publish('bbc-manual-watering', 1)
            Device_state.objects.filter(device_name="water_pump").update(state=1)
            return JsonResponse({'status': 'Độ ẩm thấp hơn mức cho phép. Đang tưới nước'})
        
        # humidity > upper threshold of humidity
        elif body["humidity"] > humi[0][1]: 
            # client.publish('bbc-manual-temperature', 1)
            Device_state.objects.filter(device_name="mini_fan").update(state=1)
            return JsonResponse({'status': 'Độ ẩm cao hơn mức cho phép. Đang thông gió'})
        
        # humidity in range
        else:
            if (Device_state.objects.filter(device_name="water_pump").values())[0]['state'] == 1:
                Device_state.objects.filter(device_name="water_pump").update(state=1) 

            elif (Device_state.objects.filter(device_name="mini_fan").values())[0]['state'] == 1:
                Device_state.objects.filter(device_name="mini_fan").update(state=1)   

            return JsonResponse({'status': 'Độ ẩm ở mức cho phép'})
    else:
        return JsonResponse({"message": "Không tìm thấy sensor"})

@csrf_exempt
@require_http_methods(['POST'])
def handleTemperature(request):
    if not checkAutoModePump() and not checkAutoModeFan():
        return JsonResponse({
            "success": False,
            "error": "Bạn đang ở chế độ thủ, không thể thực hiện hành động này."
        })
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    temp = Threshold.objects.filter(sensorID=body["sensorID"]).values_list('lowerTemp', 'upperTemp')
    if temp:
        # temperature < lower threshold of temperature
        if body["temperature"] < temp[0][0]:
            if (Device_state.objects.filter(device_name="mini_fan").values())[0]['state'] == 1:
                # client.publish('bbc-manual-temperature', 0)
                Device_state.objects.filter(device_name="mini_fan").update(state=1)
            return JsonResponse({'status': 'Nhiệt độ thấp hơn mức cho phép. Đã tắt quạt'})
        
        # temperature > upper threshold of temperature
        elif body["temperature"] > temp[0][1]:
            # client.publish('bbc-manual-temperature', 1)
            Device_state.objects.filter(device_name="mini_fan").update(state=1)

            # client.publish('bbc-manual-watering', 0)
            Device_state.objects.filter(device_name="water_pump").update(state=1)
            return JsonResponse({'status': 'Nhiệt độ cao hơn mức cho phép. Đang thông gió và tưới nước'})
        
        # temperature in range
        else:
            if (Device_state.objects.filter(device_name="water_pump").values())[0]['state'] == 1:
                Device_state.objects.filter(device_name="water_pump").update(state=1) 

            elif (Device_state.objects.filter(device_name="mini_fan").values())[0]['state'] == 1:
                Device_state.objects.filter(device_name="mini_fan").update(state=1)  
            return JsonResponse({'status': 'Nhiệt độ ở mức cho phép'})
    else:
        return JsonResponse({"message": "Không tìm thấy sensor"})
    

@csrf_exempt
@require_http_methods(['PUT'])
def toggleDeviceMode(request):
    try:
        # Parse JSON body from request
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        # Get device names and modes from the request body
        device_name = body.get("device_name")
        mode = body.get("mode")  # mode: 1 for manual, 0 for auto
        
        if not device_name or mode is None:
            return JsonResponse({"error": "Thiếu thông tin thiết bị hoặc chế độ"}, status=400)
        
        # Validate that the device exists
        device = Device_state.objects.filter(device_name=device_name).first()
        if not device:
            return JsonResponse({"error": f"Không tìm thấy thiết bị {device_name}"}, status=404)
        
        # Update the device mode
        device.manualMode = mode
        device.save()

        # Return response based on the new mode
        mode_str = "thủ công" if mode == 1 else "tự động"
        return JsonResponse({
            "success": True,
            "message": f"Chế độ của {device_name} đã được chuyển sang chế độ {mode_str}."
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)

