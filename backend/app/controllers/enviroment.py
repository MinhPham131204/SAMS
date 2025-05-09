from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from dotenv import load_dotenv
import pytz, json
from datetime import datetime
from ..models import Enviroment_log, Device_state
from django.utils import timezone
from datetime import timedelta

load_dotenv()

def format_datetime(dt_string):
    if dt_string.endswith('Z'):
        dt_string = dt_string.replace('Z', '+00:00')

    dt = datetime.fromisoformat(dt_string)

    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    dt = dt.astimezone(vietnam_tz)

    return dt.strftime("%Y/%m/%d %H:%M:%S")

@csrf_exempt
@require_http_methods(['GET'])
def get(request):
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
@require_http_methods(['POST'])
def update(request):
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
