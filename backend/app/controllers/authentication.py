from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import json
from ..models import User

load_dotenv()

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

