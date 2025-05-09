from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import json
from ..models import Threshold, Device_state

load_dotenv()

@csrf_exempt
@require_http_methods(['GET'])
def get(request):
    try:
        # Lấy dữ liệu threshold
        threshold = Threshold.objects.filter(sensorID=1).first()
        
        if not threshold:
            return JsonResponse({
                "success": False,
                "error": "Không tìm thấy threshold cho sensor này"
            }, status=404)
        
        # Lấy trạng thái thiết bị
        water_pump = Device_state.objects.filter(device_name="water_pump").first()
        mini_fan = Device_state.objects.filter(device_name="mini_fan").first()
        
        # Nếu không tìm thấy device states
        if not water_pump or not mini_fan:
            return JsonResponse({
                "success": False,
                "error": "Không tìm thấy trạng thái thiết bị"
            }, status=404)
        
        # Xây dựng cấu trúc phản hồi
        response_data = {
            "success": True,
            "data": {
                "irrigation": {
                    "mode": 1 if water_pump.manualMode else 0,
                    "device_state": water_pump.state,  # state 0 là đang tắt, state 1 là đang bật
                    "auto_threshold": {
                        "temp": {
                            "min": threshold.lowerTemp,
                            "max": threshold.upperTemp
                        },
                        "hum": {
                            "min": threshold.lowerHumidity,
                            "max": threshold.upperHumidity
                        },
                        "lig": {
                            "min": threshold.lowerLight,
                            "max": threshold.upperLight
                        },
                        "soil": {
                            "min": threshold.lowerSoil,
                            "max": threshold.upperSoil
                        }
                    }
                },
                "ventilation": {
                    "mode": 1 if mini_fan.manualMode else 0,
                    "device_state": mini_fan.state,  # state 0 là đang tắt, state 1 là đang bật
                    "auto_threshold": {
                        "temp": {
                            "min": threshold.lowerTemp,
                            "max": threshold.upperTemp
                        },
                        "hum": {
                            "min": threshold.lowerHumidity,
                            "max": threshold.upperHumidity
                        },
                        "lig": {
                            "min": threshold.lowerLight,
                            "max": threshold.upperLight
                        },
                        "soil": {
                            "min": threshold.lowerSoil,
                            "max": threshold.upperSoil
                        }
                    }
                }
            }
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(['PUT'])
def updateThreshold(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if Threshold.objects.filter(sensorID=body["sensorID"]).values():
        Threshold.objects.filter(sensorID=body["sensorID"]).update(
            lowerTemp=body["temp"]["min"],
            upperTemp=body["temp"]["max"],
            lowerHumidity=body["hum"]["min"],
            upperHumidity=body["hum"]["max"],
            lowerLight=body["lig"]["min"],
            upperLight=body["lig"]["max"],
            lowerSoil=body["soil"]["min"],
            upperSoil=body["soil"]["max"]
        )
        return JsonResponse({
            'success': True,
            'data': body
        })
    else: 
        return JsonResponse({"message": "Không tìm thấy sensor"})


@csrf_exempt
@require_http_methods(['PUT'])
def updateMode(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if body["type"] == "irrigation":
        Device_state.objects.filter(device_name="water_pump").update(manualMode=body["mode"])
        return JsonResponse({
            "success": True,
            'data': body["mode"]
        })
    elif body["type"] == "ventilation":
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
@require_http_methods(['PUT'])
def updateDeviceState(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if body["type"] == "irrigation":
        if Device_state.objects.filter(device_name="water_pump").first().manualMode: 
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
        if Device_state.objects.filter(device_name="mini_fan").first().manualMode: 
            print(Device_state.objects.filter(device_name="mini_fan").first().manualMode)
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
